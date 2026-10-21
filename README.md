# 🔎 Plausibil
### AI-Powered ESG Disclosure Monitoring

**Can we trust what companies report about sustainability?**

Plausibil is an explainable sustainability monitoring prototype that helps analysts examine corporate Environmental, Social, and Governance (ESG) disclosures, track reported emissions metrics over time, and identify unusual patterns that deserve further investigation.

Instead of treating every reported number as automatically reliable, Plausibil helps users understand **what changed, what looks unusual, and where the supporting evidence comes from.**

> Built for Sustainathon 2026.

---

## 🌍 The Problem

Companies publish sustainability and emissions disclosures, but interpreting these reports consistently can be challenging.

- **Inconsistent metrics:** Reported values may use different formats or units.
- **Unusual changes:** Large changes between reporting periods can be difficult to spot manually.
- **Limited visibility:** Annual reports alone provide relatively few observations over time.
- **Evidence gaps:** Analysts need to trace suspicious or unusual values back to their sources.

These challenges make sustainability disclosures harder to compare and investigate.

## 💡 Our Solution

Plausibil combines metric normalization, rule-based validation, and anomaly detection to help analysts review sustainability disclosures more systematically.

It turns uploaded reports and historical observations into structured metrics and review signals, helping users prioritize what needs a closer look.

**Important:** Plausibil flags patterns for human review. It does not automatically establish fraud, greenwashing, or deliberate misconduct.

## ⚙️ How It Works

The workflow can be understood in six steps:

1. **Upload a report** — Provide a company's sustainability report in PDF format.
2. **Extract information** — Retrieve report text and identify relevant metrics.
3. **Normalize metrics** — Organize reported values into a consistent structure.
4. **Check for inconsistencies** — Apply rules to identify unusual totals, intensities, and changes.
5. **Analyze historical trends** — Use periodic observations and Isolation Forest anomaly detection when sufficient data is available.
6. **Review the evidence** — Examine flagged signals alongside their supporting source evidence.

### The workflow at a glance

`PDF Report → Text Extraction → Metric Normalization → Validation → Anomaly Detection → Evidence-Based Review`

## ✨ Key Features

| Feature | What it does |
|---|---|
| 📄 Report ingestion | Processes uploaded sustainability reports |
| 📊 Metric normalization | Structures reported metrics for comparison |
| 🧮 Rule-based checks | Flags unusual totals, intensities, and period-over-period movements |
| 🤖 Anomaly detection | Uses Isolation Forest when enough complete observations are available |
| 📅 Periodic monitoring | Supports weekly, monthly, quarterly, and annual reporting periods |
| 🔎 Source evidence | Connects review signals to supporting evidence |
| 📤 CSV export | Exports normalized metrics for further analysis |
| 📈 Monitoring dashboard | Brings metrics and review signals together in one interface |

## 🏗️ System Architecture

Plausibil uses a frontend-backend architecture.

**Frontend — React + Vite**
- Presents the monitoring dashboard.
- Lets users interact with report ingestion and monitoring features.
- Displays metrics and review signals.

**Backend — FastAPI**
- Exposes API endpoints.
- Processes uploaded reports.
- Coordinates normalization, validation, and anomaly detection.
- Provides monitoring data to the frontend.

**Data and analysis**
- SQLite is the default database setup.
- PostgreSQL is also supported.
- Isolation Forest provides anomaly detection when sufficient historical observations exist.

### Data flow

`User → React Dashboard → FastAPI → Database & Analysis Pipeline → Review Signals → Dashboard`

## 🧰 Technology Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI
- **Database:** SQLite, PostgreSQL
- **Data processing:** PDF text extraction and metric normalization
- **Machine learning:** Isolation Forest
- **Development:** Node.js, npm, Uvicorn

## 🚀 Getting Started

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

## 📁 Project Structure

```text
Plausibil-Sustainathon-2026/
├── backend/          # API and analysis pipeline
├── frontend/         # Web dashboard
├── data/
│   └── raw/          # Raw input data
├── docs/             # Project documentation
├── .env.example      # Example environment configuration
├── docker-compose.yml
└── README.md
```

## ⚠️ Limitations

Plausibil is a prototype for sustainability disclosure monitoring, not a production-grade fraud detection system.

- Anomaly detection depends on the quality and availability of historical data.
- The Isolation Forest workflow requires at least eight complete periodic observations in the documented implementation.
- An unusual value is not necessarily incorrect or misleading.
- Review signals require human investigation and contextual interpretation.

The system is designed to support analysts, not replace their judgment.

---

## 🌱 Why Plausibil?

Sustainability data is only useful when people can interpret and investigate it.

Plausibil aims to make corporate disclosures easier to monitor by combining structured data, transparent checks, historical analysis, and traceable evidence.

**Make sustainability claims easier to examine — one signal at a time.**
