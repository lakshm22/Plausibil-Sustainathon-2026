from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class CompanyOut(BaseModel):
    id: int
    name: str
    sector: str
    industry: str
    identifier: str
    model_config = {"from_attributes": True}


class ReportOut(BaseModel):
    id: int
    company_id: int
    financial_year: str
    report_type: str
    reporting_frequency: str
    period_start: Optional[date]
    period_end: Optional[date]
    file_name: str
    processing_status: str
    model_config = {"from_attributes": True}


class MetricOut(BaseModel):
    id: int
    report_id: int
    metric_name: str
    raw_value: Optional[float]
    raw_unit: str
    normalized_value: Optional[float]
    normalized_unit: str
    page_number: Optional[int]
    table_reference: str
    source_text: str
    extraction_confidence: float
    data_quality_status: str
    model_config = {"from_attributes": True}


class FlagOut(BaseModel):
    id: int
    report_id: int
    flag_type: str
    severity: str
    score: float
    title: str
    description: str
    status: str
    model_config = {"from_attributes": True}


class ReportUploadMeta(BaseModel):
    company_name: str = Field(default="Uploaded Company", max_length=200)
    sector: str = Field(default="Unknown", max_length=100)
    industry: str = Field(default="Unknown", max_length=100)
    identifier: str = Field(default="", max_length=100)
    reporting_frequency: str = Field(default="monthly", pattern="^(weekly|monthly|quarterly|annual)$")
    period_start: Optional[date] = None
    period_end: Optional[date] = None
