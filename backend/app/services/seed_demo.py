from datetime import date, timedelta
from sqlalchemy import select
from app.db.database import SessionLocal
from app.models.database_models import Company, Report, Metric, Flag, Evidence


def seed_if_empty():
    db = SessionLocal()
    try:
        if db.scalar(select(Company.id).limit(1)):
            return
        c1 = Company(name="Example Industries", sector="Manufacturing", industry="Industrial Products", identifier="DEMO-01")
        c2 = Company(name="Green Materials Co.", sector="Cement", industry="Cement", identifier="DEMO-02")
        c3 = Company(name="Digital Systems Ltd.", sector="IT", industry="IT Services", identifier="DEMO-03")
        db.add_all([c1, c2, c3]); db.commit()
        for c in (c1, c2, c3): db.refresh(c)

        start = date(2025, 1, 1)
        for company_index, company in enumerate((c1, c2, c3)):
            base = 10000 if company.sector == "Manufacturing" else 8000 if company.sector == "Cement" else 1500
            production = 100000 if company.sector != "IT" else 25000
            for i in range(12):
                month_start = date(2025 + (i // 12), (i % 12) + 1, 1)
                month_end = date(month_start.year + (month_start.month == 12), 1 if month_start.month == 12 else month_start.month + 1, 1) - timedelta(days=1)
                factor = 1.0 + (0.015 * i) + (0.90 if company == c1 and i == 9 else 0)
                r = Report(company_id=company.id, financial_year=month_end.isoformat(), report_type="BRSR / Monthly sustainability snapshot", reporting_frequency="monthly", period_start=month_start, period_end=month_end, file_name=f"demo_{company.id}_2025_{i+1:02d}.pdf", processing_status="COMPLETED")
                db.add(r); db.commit(); db.refresh(r)
                vals = [
                    ("scope_1_emissions", base * 0.65 * factor, "tCO2e"),
                    ("scope_2_emissions", base * 0.35 * factor, "tCO2e"),
                    ("total_ghg_emissions", base * factor, "tCO2e"),
                    ("energy_consumption", 22000 * factor, "MWh"),
                    ("water_consumption", 450000 * factor, "kL"),
                    ("waste_generated", 1400 * factor, "t"),
                    ("production_output", production * (1 + 0.004 * i), "t"),
                    ("revenue", 500000000 * (1 + 0.01 * i), "INR"),
                ]
                for name, value, unit in vals:
                    db.add(Metric(report_id=r.id, metric_name=name, raw_value=value, raw_unit=unit, normalized_value=value, normalized_unit=unit, page_number=8, table_reference="Periodic ESG snapshot", source_text=f"Demo evidence for {name}: {value:.2f} {unit}", extraction_confidence=0.98, data_quality_status="VALID"))
                db.commit()

        # A concrete seeded review signal for the investigation screen.
        target = db.scalar(select(Report).where(Report.company_id == c1.id).order_by(Report.period_end.desc()))
        if target:
            flag = Flag(report_id=target.id, flag_type="LARGE_YOY_MOVEMENT", severity="HIGH PRIORITY", score=95, title="Periodic emissions movement warrants source review", description="The latest periodic observation is materially different from the company's recent pattern. Review operational context, methodology, units and reporting boundary before drawing conclusions.")
            db.add(flag); db.commit(); db.refresh(flag)
            m = db.scalar(select(Metric).where(Metric.report_id == target.id, Metric.metric_name == "total_ghg_emissions"))
            if m:
                db.add(Evidence(flag_id=flag.id, metric_id=m.id, page_number=m.page_number, table_reference=m.table_reference, source_text=m.source_text, raw_value=m.raw_value, normalized_value=m.normalized_value, calculation="Periodic change review signal"))
                db.commit()
    finally:
        db.close()
