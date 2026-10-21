from sqlalchemy import inspect, text
from app.db.database import engine


def ensure_sqlite_columns():
    if engine.dialect.name != "sqlite":
        return
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if "reports" not in tables:
        return
    existing = {c["name"] for c in inspector.get_columns("reports")}
    additions = {
        "reporting_frequency": "VARCHAR(20) DEFAULT 'annual'",
        "period_start": "DATE",
        "period_end": "DATE",
    }
    with engine.begin() as conn:
        for name, definition in additions.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE reports ADD COLUMN {name} {definition}"))
