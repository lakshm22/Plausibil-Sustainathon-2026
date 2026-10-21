from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.database import get_db
from app.models.database_models import Company, Report, Metric, Flag

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "companies": db.scalar(select(func.count(Company.id))) or 0,
        "reports": db.scalar(select(func.count(Report.id))) or 0,
        "metrics": db.scalar(select(func.count(Metric.id))) or 0,
        "flags": db.scalar(select(func.count(Flag.id))) or 0,
        "high_priority": db.scalar(select(func.count(Flag.id)).where(Flag.severity == "HIGH PRIORITY")) or 0,
        "review": db.scalar(select(func.count(Flag.id)).where(Flag.severity == "REVIEW")) or 0,
        "weekly_reports": db.scalar(select(func.count(Report.id)).where(Report.reporting_frequency == "weekly")) or 0,
        "monthly_reports": db.scalar(select(func.count(Report.id)).where(Report.reporting_frequency == "monthly")) or 0,
        "annual_reports": db.scalar(select(func.count(Report.id)).where(Report.reporting_frequency == "annual")) or 0,
    }


@router.get("/trend")
def trend(db: Session = Depends(get_db)):
    rows = db.execute(select(Report.period_end, Report.reporting_frequency, Metric.normalized_value).join(Metric, Metric.report_id == Report.id).where(Metric.metric_name == "total_ghg_emissions").order_by(Report.period_end, Report.id)).all()
    grouped = defaultdict(float)
    for period_end, frequency, value in rows:
        if period_end and value is not None:
            grouped[(period_end.isoformat(), frequency)] += float(value)
    return [{"period": period, "frequency": frequency, "value": round(value, 2)} for (period, frequency), value in grouped.items()]
