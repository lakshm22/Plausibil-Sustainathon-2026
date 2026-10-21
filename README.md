# Plausibil
### AI-Powered ESG Disclosure Monitoring

**Can we trust what companies report about sustainability?**

Plausibil is an AI-powered ESG disclosure monitoring prototype that helps analysts examine corporate sustainability reports, identify unusual emissions patterns, and investigate potentially inconsistent disclosures.

Combining **rule-based validation, Isolation Forest anomaly detection, and SHAP-based explainability**, Plausibil helps users move beyond simply detecting anomalies to understanding the factors contributing to them.

**Detect unusual patterns. Understand the contributing factors. Trace the evidence.**

> Built for Sustainathon 2026.

---

## The Problem

Companies publish sustainability and emissions disclosures, but interpreting these reports consistently can be challenging.

- **Inconsistent metrics:** Reported values may use different formats or units.
- **Unusual changes:** Large changes between reporting periods can be difficult to spot manually.
- **Limited visibility:** Annual reports alone provide relatively few observations over time.
- **Evidence gaps:** Analysts need to trace suspicious or unusual values back to their sources.

These challenges make sustainability disclosures harder to compare and investigate.

## Our Solution

Plausibil combines metric normalization, rule-based validation, and anomaly detection to help analysts review sustainability disclosures more systematically.

It turns uploaded reports and historical observations into structured metrics and review signals, helping users prioritize what needs a closer look.

**Important:** Plausibil flags patterns for human review. It does not automatically establish fraud, greenwashing, or deliberate misconduct.

## ⚙️ How It Works

1. **Report ingestion** — Upload sustainability reports for processing.
2. **Metric extraction and normalization** — Convert relevant reported figures into structured, comparable metrics.
3. **Rule-based validation** — Check for inconsistencies, unusual values, and significant changes.
4. **Anomaly detection** — Use Isolation Forest to identify observations that deviate from expected patterns.
5. **Explainability with SHAP** — Analyze feature contributions to help explain the model's anomaly scores or predictions.
6. **Evidence-based review** — Present flagged observations and supporting source evidence for further investigation.

### The workflow at a glance

`PDF Report → Metric Extraction → Normalization → Validation → Isolation Forest → SHAP Explanations → Evidence-Based Review`

*Anomaly detection identifies patterns worth investigating; SHAP helps explain model behavior but does not independently establish why a company reported a particular value or prove misconduct.*

## Key Features

| Feature | Description |
|---|---|
| **Report Ingestion** | Upload and process sustainability reports in PDF format. |
| **Metric Normalization** | Organize reported ESG metrics into a consistent structure for comparison. |
| **Rule-Based Validation** | Flag unusual values, inconsistencies, and significant changes in reported metrics. |
| **Anomaly Detection** | Use Isolation Forest to identify observations that deviate from expected patterns. |
| **SHAP Explainability** | Understand how input features contribute to model outputs, making anomaly analysis more interpretable. |
| **Periodic Monitoring** | Track ESG metrics across reporting periods to identify unusual trends over time. |
| **Evidence Traceability** | Link flagged observations to supporting source evidence for further investigation. |
| **CSV Export** | Export normalized metrics for further analysis. |
| **Interactive Dashboard** | Explore reported metrics, monitoring results, and anomaly signals in one place. |

## System Architecture

Plausibil uses a frontend-backend architecture.

**Frontend — React + Vite**
- Presents the monitoring dashboard.
- Lets users interact with report ingestion and monitoring features.
- Displays metrics and review signals.

**Backend — Python + FastAPI**
- Exposes API endpoints.
- Processes uploaded reports.
- Coordinates normalization, validation, and anomaly detection.
- Provides monitoring data to the frontend.

### Analysis & Explainability
- **Rule-Based Validation:** Identifies predefined inconsistencies and unusual metric changes.
- **Isolation Forest:** Detects observations that differ from learned data patterns.
- **SHAP:** Helps interpret feature contributions to model outputs, providing additional context for investigating flagged observations.

### Data Layer
- **SQLite:** Default database configuration.
- **PostgreSQL:** Supported alternative database.
- **Source Evidence:** Supports traceability between reported metrics and their originating documents.

### Data flow

`Report Upload → Data Processing → Validation → Anomaly Detection → SHAP Explanations → Dashboard Visualization`

## Technology Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI
- **Database:** SQLite, PostgreSQL
- **Data processing:** PDF text extraction and metric normalization
- **Machine learning:** Isolation Forest
- **Explainable AI:** SHAP (SHapley Additive exPlanations)
- **Development:** Node.js, npm, Uvicorn

## Getting Started

### Prerequisites

Install the following before running the project:

- Python
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/lakshm22/Plausibil-Sustainathon-2026.git
cd Plausibil-Sustainathon-2026
```

### 2. Start the backend

Open a terminal in the repository directory:

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The backend API will be available at:

- **API:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/api/health

### 3. Start the frontend

Open a second terminal in the repository directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your terminal. It is normally:

http://127.0.0.1:5173

Keep both terminals running while using the application.

## Project Structure

```text
Plausibil-Sustainathon-2026/
├── backend/          # API and analysis pipeline
├── frontend/         # Web dashboard
├── data/
│   └── raw/          # Raw input data
├── docs/             # Project documentation
├── .env.example      # Example environment configuration
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Limitations

Plausibil is a prototype for sustainability disclosure monitoring, not a production-grade fraud detection system.

- Anomaly detection depends on the quality and availability of historical data.
- The Isolation Forest workflow requires at least eight complete periodic observations in the documented implementation.
- An unusual value is not necessarily incorrect or misleading.
- Review signals require human investigation and contextual interpretation.

> **Explainable by design:** Isolation Forest helps identify unusual patterns, while SHAP helps interpret the contribution of input features to the model's output. Flags are intended to support human review, not automatically establish fraud or greenwashing.

---

## Why Plausibil?

Sustainability data is only useful when people can interpret and investigate it.

Plausibil aims to make corporate disclosures easier to monitor by combining structured data, transparent checks, historical analysis, and traceable evidence.

**Make sustainability claims easier to examine — one signal at a time.**
