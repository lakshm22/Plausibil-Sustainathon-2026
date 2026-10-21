from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.database_models import Report, Metric, Flag, Evidence
from app.ml.isolation_forest import run_isolation_forest
from app.services.validation_engine import validate_total, validate_intensity, validate_yoy

CORE_METRICS = [
    "scope_1_emissions", "scope_2_emissions", "total_ghg_emissions",
    "energy_consumption", "water_consumption", "waste_generated",
    "production_output", "revenue", "emission_intensity"
]


def _report_order(report: Report):
    return (report.period_end or report.period_start or report.created_at.date(), report.id)


def _metric_map(metrics):
    out = {}
    for m in metrics:
        if m.normalized_value is not None:
            out[m.metric_name] = m.normalized_value
    return out


def _history_rows(db: Session):
    reports = list(db.scalars(select(Report)).all())
    metrics = list(db.scalars(select(Metric)).all())
    by_report = defaultdict(list)
    for m in metrics:
        by_report[m.report_id].append(m)
    rows = []
    for r in reports:
        rows.append({"report_id": r.id, "company_id": r.company_id, "date": _report_order(r), "metrics": _metric_map(by_report[r.id])})
    return reports, rows


def _build_ml_records(rows):
    by_company = defaultdict(list)
    for row in rows:
        by_company[row["company_id"]].append(row)
    records = []
    for company_rows in by_company.values():
        company_rows.sort(key=lambda x: x["date"])
        previous = None
        for row in company_rows:
            current = row["metrics"]
            record = {"report_id": row["report_id"]}
            for key in CORE_METRICS:
                record[key] = current.get(key)
            if previous:
                for key in ["scope_1_emissions", "scope_2_emissions", "total_ghg_emissions", "energy_consumption", "water_consumption", "waste_generated", "production_output", "revenue"]:
                    old, new = previous.get(key), current.get(key)
                    record[f"yoy_{key}_change"] = ((new / old) - 1) * 100 if old not in (None, 0) and new is not None else None
            production = current.get("production_output")
            if production and production > 0:
                for key, name in [("total_ghg_emissions", "emission_intensity"), ("energy_consumption", "energy_intensity"), ("water_consumption", "water_intensity"), ("waste_generated", "waste_intensity")]:
                    if current.get(key) is not None:
                        record[name] = current[key] / production
            records.append(record)
            previous = current
    return records


def analyze_report_and_history(db: Session, report_id: int):
    reports, rows = _history_rows(db)
    current_report = db.get(Report, report_id)
    if not current_report:
        return
    current_metrics = list(db.scalars(select(Metric).where(Metric.report_id == report_id)).all())
    current_values = _metric_map(current_metrics)
    current_flags = []

    total_flag = validate_total(current_values)
    if total_flag:
        current_flags.append(total_flag)
    intensity_flag = validate_intensity(current_values)
    if intensity_flag:
        current_flags.append(intensity_flag)

    company_rows = sorted([r for r in rows if r["company_id"] == current_report.company_id], key=lambda x: x["date"])
    previous_values = {}
    if len(company_rows) >= 2:
        previous_values = company_rows[-2]["metrics"]
    current_flags.extend(validate_yoy(current_values, previous_values, threshold_pct=50))

    # Remove only auto-generated flags for this report before rebuilding them.
    db.query(Flag).filter(Flag.report_id == report_id).delete(synchronize_session=False)
    db.flush()
    for flag_data in current_flags:
        flag = Flag(report_id=report_id, **flag_data)
        db.add(flag)
        db.flush()
        evidence_metric = current_metrics[0] if current_metrics else None
        if evidence_metric:
            db.add(Evidence(
                flag_id=flag.id,
                metric_id=evidence_metric.id,
                page_number=evidence_metric.page_number,
                table_reference=evidence_metric.table_reference,
                source_text=evidence_metric.source_text,
                raw_value=evidence_metric.raw_value,
                normalized_value=evidence_metric.normalized_value,
                calculation=flag.description,
            ))

    ml = run_isolation_forest(_build_ml_records(rows))
    if ml.get("available"):
        for result in ml["results"]:
            if result["report_id"] != report_id or result["anomaly_label"] != "ANOMALY":
                continue
            score = min(100.0, max(0.0, result["model_score"] * 100.0))
            flag = Flag(
                report_id=report_id,
                flag_type="ML_ANOMALY",
                severity="HIGH PRIORITY" if score >= 75 else "REVIEW",
                score=score,
                title="Historical pattern differs from the learned peer/time-series profile",
                description=f"Isolation Forest detected an unusual feature combination (model score {result['model_score']:.3f}). This is a review signal, not a probability or finding of wrongdoing.",
            )
            db.add(flag)
            db.flush()
            if current_metrics:
                m = current_metrics[0]
                db.add(Evidence(flag_id=flag.id, metric_id=m.id, page_number=m.page_number, table_reference=m.table_reference, source_text=m.source_text, raw_value=m.raw_value, normalized_value=m.normalized_value, calculation="Isolation Forest anomaly signal"))

    db.commit()
