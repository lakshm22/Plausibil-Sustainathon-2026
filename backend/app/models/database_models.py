from datetime import datetime, date
from sqlalchemy import String, Float, Integer, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    sector: Mapped[str] = mapped_column(String(100), default="Unknown")
    industry: Mapped[str] = mapped_column(String(100), default="Unknown")
    identifier: Mapped[str] = mapped_column(String(100), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reports = relationship("Report", back_populates="company", cascade="all, delete-orphan")


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    financial_year: Mapped[str] = mapped_column(String(20), default="UNKNOWN")
    report_type: Mapped[str] = mapped_column(String(100), default="BRSR")
    reporting_frequency: Mapped[str] = mapped_column(String(20), default="annual")
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    file_name: Mapped[str] = mapped_column(String(255))
    source_url: Mapped[str] = mapped_column(String(500), default="")
    file_hash: Mapped[str] = mapped_column(String(128), default="")
    processing_status: Mapped[str] = mapped_column(String(40), default="UPLOADED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="reports")
    metrics = relationship("Metric", back_populates="report", cascade="all, delete-orphan")
    flags = relationship("Flag", back_populates="report", cascade="all, delete-orphan")


class Metric(Base):
    __tablename__ = "metrics"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    metric_name: Mapped[str] = mapped_column(String(100), index=True)
    metric_category: Mapped[str] = mapped_column(String(100), default="ESG")
    raw_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw_unit: Mapped[str] = mapped_column(String(50), default="")
    normalized_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    normalized_unit: Mapped[str] = mapped_column(String(50), default="")
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    table_reference: Mapped[str] = mapped_column(String(255), default="")
    source_text: Mapped[str] = mapped_column(Text, default="")
    extraction_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    data_quality_status: Mapped[str] = mapped_column(String(40), default="VALID")
    report = relationship("Report", back_populates="metrics")


class Feature(Base):
    __tablename__ = "features"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    feature_name: Mapped[str] = mapped_column(String(100), index=True)
    feature_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    feature_unit: Mapped[str] = mapped_column(String(50), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Flag(Base):
    __tablename__ = "flags"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    flag_type: Mapped[str] = mapped_column(String(100), index=True)
    severity: Mapped[str] = mapped_column(String(30), default="REVIEW")
    score: Mapped[float] = mapped_column(Float, default=0.0)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="OPEN")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    report = relationship("Report", back_populates="flags")


class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[int] = mapped_column(primary_key=True)
    flag_id: Mapped[int] = mapped_column(ForeignKey("flags.id"))
    metric_id: Mapped[int | None] = mapped_column(ForeignKey("metrics.id"), nullable=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    table_reference: Mapped[str] = mapped_column(String(255), default="")
    source_text: Mapped[str] = mapped_column(Text, default="")
    raw_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    normalized_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    calculation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BoundaryChange(Base):
    __tablename__ = "boundary_changes"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    previous_report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    current_report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    change_description: Mapped[str] = mapped_column(Text)
    detected_change: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(String(30), default="REVIEW")
    evidence: Mapped[str] = mapped_column(Text, default="")
