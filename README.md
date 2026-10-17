# Plausibil
### Explainable Corporate Sustainability Disclosure Plausibility Platform

**An AI-powered platform for analyzing the plausibility, consistency, and traceability of corporate sustainability disclosures.**

Plausibil is a sustainability disclosure analysis platform designed to help reviewers examine corporate environmental claims, identify unusual emission patterns, and investigate inconsistencies in reported data. By combining document processing, statistical anomaly detection, and explainability techniques, the platform aims to make sustainability disclosure review more transparent and evidence-driven.

Rather than treating an anomaly as proof of wrongdoing, Plausibil provides review signals that help users identify disclosures that may warrant further investigation.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Our Solution](#our-solution)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Responsible AI and Limitations](#responsible-ai-and-limitations)
- [Future Scope](#future-scope)
- [SDG Alignment](#sdg-alignment)
- [Team](#team)
- [License](#license)

---

## Overview

Corporate sustainability and greenhouse gas emissions disclosures play an important role in evaluating environmental performance. However, reviewing these disclosures can be challenging when information is distributed across lengthy reports, presented in inconsistent formats, or difficult to compare across reporting periods.

Plausibil aims to simplify this process by providing a structured workspace for examining sustainability disclosures and surfacing potentially inconsistent or unusual data points.

The platform combines document extraction, data analysis, anomaly detection, and explainability to support human-led review.

**Project type:** Hackathon project  
**Domain:** Sustainability Analytics / ESG Technology  
**Focus:** Corporate emissions disclosures and plausibility analysis  
**Primary objective:** Explainable and evidence-oriented disclosure validation

## Problem Statement

**PS-13-S1: Are Corporate Emissions Disclosures Even Plausible?**

Organizations publish sustainability reports containing information about greenhouse gas emissions, environmental performance, and sustainability targets. Assessing these disclosures can require significant manual effort, especially when reviewers need to compare figures, identify irregularities, and trace findings back to supporting evidence.

A reported value may appear unusual for several reasons, including changes in reporting methodology, operational differences, incomplete information, or potential inconsistencies. Identifying these cases requires more than simply checking whether a number is present in a report.

The challenge is to develop a practical platform that can help reviewers:

- Extract relevant information from sustainability documents.
- Examine reported emissions and related metrics.
- Identify unusual patterns and potential inconsistencies.
- Understand why a data point has been flagged.
- Trace observations back to their supporting evidence.

## Our Solution

Plausibil approaches sustainability disclosure review as an **explainable plausibility analysis problem**.

The proposed workflow combines document processing with structured data analysis and anomaly detection. Instead of producing an unsupported verdict about a company's environmental claims, the platform highlights observations that deserve closer examination.

Its design emphasizes three principles:

1. **Plausibility over accusation:** An unusual value is a signal for review, not proof of misconduct.
2. **Explainability over black-box predictions:** Analytical findings should be accompanied by understandable reasons.
3. **Evidence over unsupported conclusions:** Findings should be traceable to the available source material whenever possible.

## Key Features

The following describes the intended capabilities of the platform. Individual features should be marked as implemented only when they are available in the current build.

### 1. Sustainability Document Processing

Process sustainability reports and extract relevant text and tabular information for further analysis.

- PDF text extraction.
- Support for tabular data extraction.
- OCR-assisted processing for scanned documents, where configured.
- Preparation of extracted information for structured analysis.

### 2. Emissions Data Analysis

Examine reported environmental metrics to identify values and patterns that may warrant additional review.

- Analyze available emissions-related data.
- Compare relevant values when sufficient comparable data exists.
- Identify potential inconsistencies in the available information.
- Support structured examination of reported metrics.

### 3. Anomaly Detection

Use statistical or machine-learning techniques to identify observations that differ from patterns in the analyzed data.

- Detect unusual data points using Isolation Forest.
- Surface potential anomalies for human review.
- Support investigation of unexpected patterns.
- Avoid treating statistical outliers as definitive evidence of incorrect reporting.

### 4. Explainable Findings

Use explainability techniques, including SHAP where applicable, to help reviewers understand model behavior.

- Provide interpretable information about relevant model features.
- Help users investigate why an observation received attention.
- Distinguish analytical signals from verified facts.
- Support transparent review rather than unexplained automated judgments.

### 5. Evidence-Oriented Review

Keep the relationship between an analytical observation and its source information central to the workflow.

- Retain source references when extraction and processing provide them.
- Enable reviewers to inspect the underlying information.
- Support verification of extracted values against available documents.

**Important:** The accuracy of these capabilities depends on the available data, extraction quality, model configuration, and implemented validation logic.

## How It Works

The intended processing pipeline follows these stages:

1. **Document input:** Provide a corporate sustainability or emissions disclosure.
2. **Document extraction:** Extract relevant text, tables, and other supported information.
3. **Data preparation:** Organize extracted information into a structured representation suitable for analysis.
4. **Plausibility analysis:** Examine relevant metrics and identify potential inconsistencies or unusual patterns.
5. **Anomaly detection:** Apply configured statistical or machine-learning methods to suitable data.
6. **Explainability:** Generate interpretable information about flagged observations where supported.
7. **Human review:** Inspect the findings and refer to the source evidence before drawing conclusions.

The output is intended to support investigation and review, not automatically determine whether a disclosure is true or false.

## Technology Stack

The planned technology stack is organized into the following components.

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React, Vite | User interface and application development |
| Styling | Tailwind CSS | Responsive interface styling |
| Data visualization | Recharts | Visual representation of analytical results |
| HTTP communication | Axios | Frontend-to-backend requests |
| Backend | FastAPI | API development and request handling |
| Data validation | Pydantic | Request and response validation |
| Application server | Uvicorn | Running the FastAPI application |
| PDF processing | PyMuPDF, pdfplumber | Extracting information from PDF documents |
| OCR | Tesseract | Text extraction from supported scanned documents |
| Data analysis | Pandas, NumPy | Data preparation and numerical analysis |
| Anomaly detection | Isolation Forest | Identifying unusual observations |
| Explainability | SHAP | Interpreting supported model predictions |
| Database | PostgreSQL / Supabase | Structured data persistence, where configured |

The final dependencies and deployment configuration should reflect the versions and services actually used in the repository.

## System Architecture

Plausibil is designed around a frontend, an analysis API, and a document-processing and analytics workflow.

```text
                 ┌──────────────────────────┐
                 │          User            │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ React + Vite Frontend    │
                 │ Tailwind CSS / Recharts  │
                 └────────────┬─────────────┘
                              │ HTTP / API
                              ▼
                 ┌──────────────────────────┐
                 │       FastAPI Backend    │
                 │   Pydantic Validation    │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Document Processing      │
                 │ PDF Extraction / OCR     │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Data Preparation         │
                 │ Pandas / NumPy           │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Plausibility Analysis    │
                 │ Isolation Forest / SHAP  │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Reviewable Findings      │
                 │ Evidence / Explanations  │
                 └──────────────────────────┘
```

PostgreSQL or Supabase can provide persistence for supported application data. The diagram represents the intended logical workflow; it does not imply that every component or integration is already implemented.

## Getting Started

Follow these instructions after confirming the actual directory structure and dependencies in your local repository.

### Prerequisites

- Node.js and npm
- Python 3.10 or a version supported by the backend dependencies
- Git
- PostgreSQL or Supabase, if database integration is enabled
- Tesseract OCR, if OCR-based extraction is enabled

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your repository URL and project directory.

### 2. Set Up the Frontend

Navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

If the frontend is located at the repository root rather than in a `frontend` directory, run these commands from the appropriate location.

Vite will display the local development URL in the terminal.

### 3. Set Up the Backend

Open a separate terminal and navigate to the backend directory:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI application using the actual Python module and application variable defined in the repository. For example, if the entry point is `main.py` and exposes `app`:

```bash
uvicorn main:app --reload
```

The API documentation is typically available at `/docs` when FastAPI's interactive documentation is enabled.

### 4. Configure Environment Variables

If the application requires database credentials, API settings, or other configuration, create a local `.env` file using the variable names expected by the application.

Example placeholders:

```env
DATABASE_URL=your_database_connection_string
```

Only include variables that the current implementation actually uses.

**Never commit real credentials, database passwords, access tokens, or private environment files to GitHub.** Provide a sanitized `.env.example` for required configuration instead.

## Project Structure

The following is an illustrative structure for the proposed stack. Adapt it to match the actual repository.

```text
Plausibil/
├── frontend/
├── backend/
├── docs
├── data
├── .env.example
├── README.md
├── LICENSE
└── .gitignore
```

This is a reference layout, not a claim that these exact files already exist.

## Responsible AI and Limitations

Plausibil is intended to assist sustainability disclosure review, not replace professional judgment or independent verification.

### What the platform aims to do

- Highlight potentially unusual or inconsistent information.
- Provide interpretable analytical signals where supported.
- Help reviewers examine source documents and extracted data.
- Make the review process more structured and transparent.

### What the platform does not establish

- Whether a company has committed fraud or intentionally misrepresented information.
- Whether a reported emissions figure is definitively true or false.
- Whether a flagged observation necessarily indicates an error.
- Whether the absence of an anomaly proves that a disclosure is accurate.

Anomaly detection depends on the data and assumptions used. Missing context, inconsistent reporting boundaries, changing measurement methods, poor-quality OCR, and limited comparison data can all affect the results.

SHAP explanations describe aspects of model behavior; they do not independently verify a disclosure or establish causation.

All flagged observations should therefore be interpreted as **review signals requiring contextual assessment and, where appropriate, independent verification**.

## Future Scope

Potential extensions include:

- Broader support for sustainability report formats.
- Improved extraction and validation of emissions-related tables.
- Comparisons across reporting periods when comparable data is available.
- More comprehensive source-level evidence traceability.
- Improved visualization of anomalies and supporting metrics.
- Evaluation of detection methods against curated, documented test cases.
- Additional validation for different reporting methodologies and organizational contexts.

These items represent possible future improvements, not necessarily features currently available.

## SDG Alignment

Plausibil aligns with the United Nations Sustainable Development Goal 13: **Climate Action**.

By supporting the examination of corporate emissions disclosures, the project aims to contribute to more transparent and evidence-oriented environmental reporting. Its focus is on improving the process of reviewing sustainability information, rather than claiming to independently measure or verify an organization's environmental impact.

## Team

Developed by a two-member team as a hackathon project.

- **Team size:** 2
- **Focus areas:** Sustainability analytics, document processing, explainable machine learning, and full-stack application development.

Add contributor names and GitHub profile links here if the team members wish to make them public.

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to the conditions of the license.

See the `LICENSE` file for the complete license terms.

---

*Plausibil — Making sustainability disclosure review more explainable, traceable, and evidence-driven.*