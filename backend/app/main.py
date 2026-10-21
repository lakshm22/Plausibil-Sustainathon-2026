from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
from app.db.migrations import ensure_sqlite_columns
from app.api.routes import health, companies, reports, metrics, flags, dashboard, analysis
from app.services.seed_demo import seed_if_empty

# Prototype-friendly schema bootstrap. The SQLite migration keeps an older local DB usable.
Base.metadata.create_all(bind=engine)
ensure_sqlite_columns()

app = FastAPI(title="Plausibil API", version="0.2.0", description="Explainable corporate sustainability disclosure plausibility analysis.")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
if "http://127.0.0.1:5173" not in origins:
    origins.append("http://127.0.0.1:5173")
app.add_middleware(CORSMiddleware, allow_origins=origins or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health.router, prefix="/api")
app.include_router(companies.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(flags.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")


@app.on_event("startup")
def startup():
    seed_if_empty()
