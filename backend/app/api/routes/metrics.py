import csv, io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.models.database_models import Metric
from app.schemas.api_schemas import MetricOut

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=list[MetricOut])
def metrics(db: Session = Depends(get_db)):
    stmt = select(Metric).order_by(Metric.id.desc()).limit(1000)
    return list(db.scalars(stmt).all())


@router.get("/export.csv")
def export_csv(db: Session = Depends(get_db)):
    rows = list(db.scalars(select(Metric).order_by(Metric.id)).all())
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "report_id", "metric", "raw_value", "raw_unit", "normalized_value", "normalized_unit", "page", "table", "confidence", "quality"])
    for m in rows:
        writer.writerow([m.id, m.report_id, m.metric_name, m.raw_value, m.raw_unit, m.normalized_value, m.normalized_unit, m.page_number, m.table_reference, m.extraction_confidence, m.data_quality_status])
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=plausibil_normalized_data.csv"})
