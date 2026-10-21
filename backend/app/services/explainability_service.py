"""
Explainability and mitigation helpers for Plausibil review flags.

The anomaly model is still Isolation Forest. This module adds a transparent,
per-flag explanation by fitting the same feature pipeline used by the detector
and, when SHAP can explain the fitted trees, returning local feature
contributions plus human-readable interpretation. A deterministic fallback is
kept so the Investigation page never fabricates SHAP values.
"""
from collections import defaultdict
from typing import Any

import numpy as np

from app.models.database_models import Flag, Report
from app.services.analysis_pipeline import _history_rows, _build_ml_records
from app.ml.isolation_forest import DEFAULT_FEATURES
from sklearn.ensemble import IsolationForest


def _feature_label(name: str) -> str:
    labels = {
        "yoy_total_ghg_emissions_change": "YoY total GHG emissions change",
        "yoy_energy_consumption_change": "YoY energy consumption change",
        "yoy_water_consumption_change": "YoY water consumption change",
        "yoy_waste_generated_change": "YoY waste generated change",
        "emission_intensity": "Emission intensity",
        "energy_intensity": "Energy intensity",
        "water_intensity": "Water intensity",
        "waste_intensity": "Waste intensity",
        "yoy_production_output_change": "YoY production output change",
        "yoy_revenue_change": "YoY revenue change",
    }
    return labels.get(name, name.replace("_", " ").title())


def _interpret(name: str, value: float, contribution: float) -> str:
    direction = "positive" if contribution > 0 else "negative" if contribution < 0 else "neutral"
    if name.startswith("yoy_"):
        return f"{_feature_label(name)} is {value:+.1f}%; it has a {direction} SHAP contribution to the fitted model output."
    return f"{_feature_label(name)} is {value:.3f}; it has a {direction} SHAP contribution to the fitted model output."


def model_explanation(db, report_id: int) -> dict[str, Any]:
    reports, rows = _history_rows(db)
    records = _build_ml_records(rows)
    usable = []
    matrix = []
    for record in records:
        values = [record.get(name) for name in DEFAULT_FEATURES]
        if all(v is not None and np.isfinite(v) for v in values):
            usable.append(record)
            matrix.append(values)

    if len(matrix) < 8:
        return {
            "available": False,
            "method": "Isolation Forest",
            "features": [],
            "note": f"SHAP explanation needs at least 8 complete periodic observations; only {len(matrix)} complete observations are available.",
        }

    target_index = next((i for i, r in enumerate(usable) if r["report_id"] == report_id), None)
    if target_index is None:
        return {
            "available": False,
            "method": "Isolation Forest",
            "features": [],
            "note": "This flag's report does not have enough complete feature values for a local SHAP explanation.",
        }

    X = np.asarray(matrix, dtype=float)
    model = IsolationForest(n_estimators=300, contamination="auto", random_state=42)
    model.fit(X)

    contributions = None
    method = "SHAP TreeExplainer"
    shap_note = "Local feature contributions from the fitted Isolation Forest trees."

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(X)
        if isinstance(values, list):
            values = values[0]
        arr = np.asarray(values)
        if arr.ndim == 3:
            arr = arr[0]
        contributions = arr[target_index]
    except Exception as exc:
        method = "Model feature deviation fallback"
        shap_note = f"SHAP could not be evaluated for this fitted model ({type(exc).__name__}); showing transparent standardized deviation instead."

    feature_values = X[target_index]
    medians = np.median(X, axis=0)
    stds = np.std(X, axis=0)
    features = []

    for i, name in enumerate(DEFAULT_FEATURES):
        value = float(feature_values[i])
        median = float(medians[i])
        std = float(stds[i])
        if contributions is not None:
            contribution = float(contributions[i])
            magnitude = abs(contribution)
            explanation = _interpret(name, value, contribution)
        else:
            z = (value - median) / std if std > 1e-9 else 0.0
            contribution = float(z)
            magnitude = abs(contribution)
            explanation = f"{_feature_label(name)} is {value:.3f}, about {z:+.2f} standard deviations from the observed median."

        features.append({
            "feature": _feature_label(name),
            "feature_key": name,
            "value": value,
            "baseline": median,
            "contribution": contribution,
            "magnitude": magnitude,
            "direction": "positive" if contribution > 0 else "negative" if contribution < 0 else "neutral",
            "interpretation": explanation,
        })

    features.sort(key=lambda x: x["magnitude"], reverse=True)
    return {
        "available": True,
        "method": method,
        "features": features[:6],
        "observation_count": len(usable),
        "model_version": "isolation-forest-v2-periodic",
        "note": shap_note,
    }


MITIGATIONS = {
    "INTERNAL_TOTAL_MISMATCH": [
        ("Reconcile the emissions ledger", "Recalculate Scope 1 + Scope 2 from the source tables and document any separately reported categories or exclusions.", "ESG / Sustainability"),
        ("Confirm reporting boundary", "Check whether the reported total uses the same organizational and operational boundary as the component values.", "ESG + Finance"),
        ("Validate units and rounding", "Confirm all component values use the same units and precision before reconciliation.", "Data / Reporting"),
    ],
    "INTENSITY_MISMATCH": [
        ("Recalculate the intensity KPI", "Recompute emissions divided by the stated production/output denominator and compare it with the published intensity.", "ESG / Data"),
        ("Validate denominator definition", "Confirm production/output scope, period and units match the emissions period and boundary.", "Operations + ESG"),
        ("Document methodology changes", "If methodology or denominator definitions changed, record the change and provide a like-for-like comparison where possible.", "ESG / Reporting"),
    ],
    "LARGE_YOY_MOVEMENT": [
        ("Perform variance review", "Trace the change to operational drivers, acquisitions/divestments, production changes, weather, shutdowns or other documented causes.", "Operations + ESG"),
        ("Check boundary and methodology continuity", "Compare the current and prior-period organizational boundary, calculation methodology and emission factors.", "ESG / Assurance"),
        ("Add periodic monitoring", "Continue weekly or monthly observations so large movements can be distinguished from one-off reporting effects.", "ESG / Data"),
    ],
    "ML_ANOMALY": [
        ("Inspect the top contributing features", "Review the highest-impact features and their source values before deciding whether the anomaly is operational or data-related.", "ESG / Data"),
        ("Validate source and units", "Check the source page, units, normalization and extraction confidence for the affected metrics.", "Data / Reporting"),
        ("Collect more periodic observations", "Use consistent weekly or monthly observations to give the anomaly model a stronger company-specific baseline.", "ESG / Data"),
    ],
}


def mitigation_recommendations(flag: Flag, model_explanation: dict[str, Any] | None = None) -> dict[str, Any]:
    actions = list(MITIGATIONS.get(flag.flag_type, [
        ("Validate source evidence", "Review the cited report page, table, units and extracted values against the original disclosure.", "ESG / Assurance"),
        ("Check reporting context", "Confirm reporting boundary, period, methodology and operational context for the flagged observation.", "ESG / Operations"),
        ("Document the resolution", "Record the verified explanation, correction or supporting evidence so the review trail remains auditable.", "ESG / Reporting"),
    ]))

    top = (model_explanation or {}).get("features", [])[:2]
    if flag.flag_type == "ML_ANOMALY" and top:
        names = ", ".join(item["feature"] for item in top)
        actions[0] = (
            "Review the highest-impact features",
            f"Start with {names}. Compare the current values with the company's historical baseline and the source disclosure.",
            "ESG / Data",
        )

    return {
        "available": True,
        "title": "Recommended mitigation & resolution actions",
        "note": "These are review-oriented actions, not automatic corrections or conclusions about the company.",
        "actions": [
            {"step": i + 1, "action": a, "detail": d, "owner": o}
            for i, (a, d, o) in enumerate(actions)
        ],
    }
