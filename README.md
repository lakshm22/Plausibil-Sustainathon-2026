# Plausibil — Periodic ESG Disclosure Monitoring Prototype

Plausibil is an explainable corporate sustainability disclosure monitoring prototype. It is designed to help an analyst/auditor monitor **weekly, monthly, quarterly and annual observations**, normalize reported metrics, surface internal inconsistencies, and investigate review signals with source evidence.

## What changed in this version

- Redesigned dashboard inspired by the supplied Plausibil reference UI.
- Working FastAPI + React/Vite integration.
- SQLite-first setup; PostgreSQL remains supported.
- Fixed SQLAlchemy result handling (`.limit()` is applied to the SQL statement before execution).
- Periodic report model with `reporting_frequency`, `period_start`, and `period_end`.
- Monthly demo observations seeded automatically so the dashboard is useful immediately.
- Weekly/monthly/quarterly/annual ingestion controls in the UI.
- Periodic time-series feature engineering for anomaly detection.
- Isolation Forest uses periodic changes and intensity features when enough complete observations exist.
- Rule-based checks for totals, intensity and large period-over-period movements.
- Source evidence is linked to review signals.
- Partial frontend loading: if one API endpoint fails, the rest of the dashboard can still load and the failing endpoint is named.
- CSV export for normalized metrics.

## Product framing

Plausibil generates **review signals**, not findings of wrongdoing. A model score is not a probability. Human review is required before drawing conclusions from a signal.

## Why periodic data?

Annual reports provide valuable disclosure context but only a small number of observations. Weekly/monthly snapshots can provide more temporal observations, making it possible to detect changes between annual disclosures and give a time-series anomaly model more training examples. More data does **not automatically guarantee higher model accuracy**; the value depends on data quality, coverage, consistency and the relevance of the features.

The prototype therefore keeps annual reports as an anchor while allowing more frequent observations as additional evidence.

## Windows / PowerShell quick start

### Backend

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`
Health: `http://127.0.0.1:8000/api/health`

### Frontend

Open a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://127.0.0.1:5173`.

### If you already have an older SQLite database

The backend includes a small SQLite compatibility migration that adds the periodic-report columns when they are missing. For a completely clean demo, you can also delete `backend/plausibil.db` and restart the backend; the demo dataset will be seeded again.

## Ingestion flow

1. Select a PDF in **Report Ingestion**.
2. Enter company and reporting cadence.
3. Optionally provide period start/end dates.
4. FastAPI stores the report and processes it in the background.
5. PDF text is extracted.
6. Metrics are normalized.
7. Rule-based checks run.
8. Historical periodic observations are assembled.
9. Isolation Forest is run when enough complete observations exist.
10. Review signals receive source evidence.

## Notes on the ML prototype

The model intentionally uses a conservative minimum of 8 complete periodic observations for the Isolation Forest path. With fewer observations, the API reports that ML is unavailable rather than pretending that a tiny sample is reliable.

The model features include period-over-period changes and intensity features. This is a prototype for monitoring, not a validated production fraud detector.
