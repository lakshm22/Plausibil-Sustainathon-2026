from pathlib import Path
from datetime import date
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, Form
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.core.config import settings
from app.models.database_models import Company, Report, Metric, Flag
from app.schemas.api_schemas import ReportOut
from app.services.pdf_extractor import extract_pdf, file_hash
from app.services.metric_extractor import extract_metrics
from app.services.normalization_service import normalize_metric
from app.services.analysis_pipeline import analyze_report_and_history

router = APIRouter(prefix="/reports", tags=["reports"])


def process_report(report_id: int):
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        report = db.get(Report, report_id)
        if not report:
            return
        report.processing_status = "EXTRACTING"
        db.commit()
        path = Path(settings.upload_dir) / report.file_name
        pages = extract_pdf(str(path))
        extracted = extract_metrics(pages)
        report.processing_status = "NORMALIZING"
        db.query(Metric).filter(Metric.report_id == report.id).delete(synchronize_session=False)
        for item in extracted:
            db.add(Metric(report_id=report.id, **normalize_metric(item)))
        db.commit()
        report.processing_status = "ANALYZING"
        db.commit()
        analyze_report_and_history(db, report.id)
        report.processing_status = "COMPLETED"
        db.commit()
    except Exception as exc:
        if report:
            report.processing_status = "FAILED"
            db.commit()
        print(f"Plausibil report processing failed for {report_id}: {exc}")
    finally:
        db.close()


@router.post("/upload", response_model=ReportOut)
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company_name: str = Form("Uploaded Company"),
    sector: str = Form("Unknown"),
    industry: str = Form("Unknown"),
    identifier: str = Form(""),
    reporting_frequency: str = Form("monthly"),
    period_start: str | None = Form(None),
    period_end: str | None = Form(None),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported.")
    if reporting_frequency not in {"weekly", "monthly", "quarterly", "annual"}:
        raise HTTPException(400, "reporting_frequency must be weekly, monthly, quarterly, or annual.")

    try:
        start = date.fromisoformat(period_start) if period_start else None
        end = date.fromisoformat(period_end) if period_end else None
    except ValueError:
        raise HTTPException(400, "period_start and period_end must use YYYY-MM-DD.")

    company = db.scalar(select(Company).where(Company.identifier == identifier)) if identifier else None
    if not company:
        company = Company(name=company_name or "Uploaded Company", sector=sector or "Unknown", industry=industry or "Unknown", identifier=identifier or str(uuid.uuid4())[:8])
        db.add(company)
        db.commit()
        db.refresh(company)

    safe_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    path = Path(settings.upload_dir) / safe_name
    path.write_bytes(await file.read())
    label = end.isoformat() if end else "UNKNOWN"
    report = Report(
        company_id=company.id,
        financial_year=label,
        report_type="BRSR/Sustainability",
        reporting_frequency=reporting_frequency,
        period_start=start,
        period_end=end,
        file_name=safe_name,
        file_hash=file_hash(str(path)),
        processing_status="UPLOADED",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    background_tasks.add_task(process_report, report.id)
    return report


@router.post("/{report_id}/process")
def process(report_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if not report:
        raise HTTPException(404, "Report not found")
    background_tasks.add_task(process_report, report.id)
    return {"status": "processing", "report_id": report.id}


@router.get("", response_model=list[ReportOut])
def reports(db: Session = Depends(get_db)):
    return list(db.scalars(select(Report).order_by(Report.id.desc())).all())
