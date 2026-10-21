from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.database import get_db
from app.models.database_models import Company
from app.schemas.api_schemas import CompanyOut

router=APIRouter(prefix="/companies", tags=["companies"])

@router.get("", response_model=list[CompanyOut])
def companies(db: Session=Depends(get_db)):
    return list(db.scalars(select(Company).order_by(Company.name)))
