from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.models.database_models import Report, Metric, Flag

router=APIRouter(prefix="/analyze", tags=["analysis"])

@router.post("/{report_id}")
def analyze(report_id:int, db:Session=Depends(get_db)):
    report=db.get(Report,report_id)
    if not report: raise HTTPException(404,"Report not found")
    metrics=list(db.scalars(select(Metric).where(Metric.report_id==report_id)))
    values={m.metric_name:m.normalized_value for m in metrics}
    created=[]
    s1,s2,total=values.get("scope_1_emissions"),values.get("scope_2_emissions"),values.get("total_ghg_emissions")
    if all(v is not None for v in (s1,s2,total)) and total:
        diff=abs((s1+s2-total)/total)*100
        if diff>2:
            f=Flag(report_id=report_id,flag_type="INTERNAL_TOTAL_MISMATCH",severity="HIGH PRIORITY",score=min(100,diff),title="Reported total does not reconcile",description=f"Scope 1 + Scope 2 differs from reported total by {diff:.1f}%. Review source values, rounding and boundary definitions.")
            db.add(f); created.append(f)
    db.commit()
    return {"report_id":report_id,"flags_created":len(created),"message":"Rule-based analysis completed."}
