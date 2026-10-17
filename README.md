# Plausibil
### Explainable Corporate Sustainability Disclosure Plausibility Platform

**Making corporate sustainability disclosure review more explainable, traceable, and evidence-driven.**

Plausibil is a sustainability disclosure analysis platform designed to help reviewers examine corporate environmental and greenhouse gas emissions disclosures. It focuses on identifying unusual patterns, highlighting potential inconsistencies, and supporting evidence-oriented review through document processing and explainable analytical techniques.

Developed as a two-member hackathon project, Plausibil explores how data analysis and machine learning can support more structured sustainability disclosure assessment.

> **An anomaly is a signal for further investigation, not proof of fraud or deliberate misreporting.**

## Problem Statement

**PS-13-S1: Are Corporate Emissions Disclosures Even Plausible?**

Corporate sustainability disclosures are important for understanding environmental performance. However, reviewing them can require significant manual effort, particularly when information is distributed across lengthy documents, presented in inconsistent formats, or difficult to compare.

Plausibil addresses this challenge by exploring ways to:

- Extract relevant information from sustainability reports.
- Examine reported emissions and related environmental metrics.
- Identify unusual observations and potential inconsistencies.
- Make analytical findings easier to interpret.
- Support investigation through available source evidence.

## Proposed Solution

Plausibil approaches sustainability disclosure assessment as an **explainable plausibility analysis problem**.

The platform is designed to combine document processing, structured data analysis, anomaly detection, and explainability techniques to surface observations that may warrant closer examination.

Its approach emphasizes three principles:

- **Plausibility over accusation:** Unusual values are review signals, not proof of wrongdoing.
- **Explainability over black-box predictions:** Findings should be understandable wherever the analytical method supports it.
- **Evidence over unsupported conclusions:** Reviewers should be able to examine the underlying source information where available.

## Key Features

The following capabilities describe the project's intended scope. Their actual availability depends on the implementation in the repository.

### Document Processing
- PDF text extraction.
- Extraction of relevant tabular information.
- OCR-assisted processing for supported scanned documents, where configured.
- Preparation of extracted information for analysis.

### Emissions Data Analysis
- Examination of available emissions-related metrics.
- Identification of potentially unusual values and patterns.
- Comparison of relevant observations when sufficient comparable data exists.

### Anomaly Detection
- Planned use of Isolation Forest for identifying unusual observations.
- Flagging of potential anomalies for further review.
- Analysis of patterns without treating statistical outliers as definitive evidence of incorrect reporting.

### Explainable Analysis
- Exploration of SHAP for interpreting supported model predictions.
- More transparent presentation of analytical signals.
- Support for human-led investigation rather than unexplained automated judgments.

### Evidence-Oriented Review
- Association of findings with source information where supported by the implementation.
- Support for checking extracted information against available documents.
- Emphasis on traceability and contextual assessment.

## How It Works

1. **Document input:** Provide a supported sustainability or emissions disclosure.
2. **Document extraction:** Extract relevant text and tables.
3. **Data preparation:** Organize extracted information for analysis.
4. **Plausibility analysis:** Examine metrics and identify potential inconsistencies.
5. **Anomaly detection:** Apply suitable detection methods to the available data.
6. **Explainability:** Provide interpretable information about findings where supported.
7. **Human review:** Examine the evidence and determine whether further investigation is necessary.

The quality of the results depends on extraction accuracy, data completeness, model configuration, and the context in which the reported values are interpreted.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite |
| Styling | Tailwind CSS |
| Visualization | Recharts |
| API communication | Axios |
| Backend | Python, FastAPI |
| Data validation | Pydantic |
| PDF processing | PyMuPDF, pdfplumber |
| OCR | Tesseract |
| Data analysis | Pandas, NumPy |
| Anomaly detection | Isolation Forest |
| Explainability | SHAP |
| Database | SQLite in the earlier setup |

The table reflects the project's discussed technology stack. Confirm the actual dependencies against the repository before treating every listed component as implemented.

## Architecture

```text
           ┌───────────────────────┐
           │         User          │
           └───────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ React + Vite Frontend │
           └───────────┬───────────┘
                       │ HTTP / API
                       ▼
           ┌───────────────────────┐
           │    FastAPI Backend    │
           └───────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ Document Processing   │
           │ and Data Preparation  │
           └───────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ Plausibility Analysis │
           │ and Anomaly Detection │
           └───────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ Reviewable Findings   │
           │ and Source Evidence   │
           └───────────────────────┘
```

This diagram represents the intended logical workflow. The actual data flow and implemented modules should be verified against the current codebase.

## Getting Started

### Prerequisites

- Node.js and npm
- Python and pip
- Git

Additional system dependencies may be required if OCR or other optional components are enabled.

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your repository URL and directory name.

### Frontend Setup

Navigate to the directory containing the frontend's `package.json` file.

```bash
npm install
npm run dev
```

Open the local URL displayed by Vite.

### Backend Setup

Navigate to the backend directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies if a `requirements.txt` file is present:

```bash
pip install -r requirements.txt
```

Start the application using the actual FastAPI entry point. For example, if the application object is named `app` in `main.py`:

```bash
uvicorn main:app --reload
```

When enabled, FastAPI's interactive API documentation is typically available at `/docs`.

**Note:** Adjust directory names, entry points, and commands to match the actual repository.

## Project Structure

The following is a high-level illustration. Replace it with the exact directory structure if the repository differs.

```text
Plausibil/
├── frontend/
│   └── ...                  # React + Vite application
├── backend/
│   └── ...                  # FastAPI application
├── README.md
├── LICENSE
└── .gitignore
```

## Responsible AI and Limitations

Plausibil is intended to assist sustainability disclosure review, not replace human judgment or independent verification.

- An anomaly does not prove fraud, deception, or deliberate misreporting.
- Unusual values can have legitimate operational or methodological explanations.
- Poor-quality document extraction can introduce errors.
- Incomplete data can affect comparisons and analytical results.
- Explainability methods describe aspects of model behavior; they do not independently establish factual correctness.
- The absence of an anomaly does not guarantee that a disclosure is accurate.

All findings should be interpreted as review signals requiring contextual assessment and, where appropriate, independent verification.

## Future Scope

Potential improvements include:

- Expanded support for sustainability report formats.
- Improved extraction and validation of emissions-related tables.
- Comparisons across reporting periods where data is comparable.
- Better source-level evidence traceability.
- Additional visualizations for analytical findings.
- Evaluation against documented test datasets.
- Improved handling of different reporting methodologies.

These are potential extensions, not claims about currently implemented features.

## SDG Alignment

Plausibil aligns with **United Nations Sustainable Development Goal 13: Climate Action**.

By supporting the structured examination of corporate emissions disclosures, the project explores how technology can contribute to more transparent and evidence-oriented sustainability reporting.

Plausibil focuses on analyzing disclosed information; it does not independently measure a company's environmental impact or certify its emissions data.

## Team

Plausibil was developed by a two-member team as a hackathon project.

| Contributor | GitHub Profile |
|---|---|
| Lakshitha Mathiyalagan (Project Design & Development) | [@lakshm22](https://github.com/lakshm22) |
| V. C. Keerthanapriya (Testing & Validation) | [@keeyaa-3](https://github.com/keeyaa-3) |


## License

This project is licensed under the **MIT License**.

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to the terms of the license.

See the [LICENSE](LICENSE) file for the complete license text.

---

*Plausibil — Explainable analysis for more transparent sustainability disclosure review.*
