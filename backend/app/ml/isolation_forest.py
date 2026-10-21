import numpy as np
from sklearn.ensemble import IsolationForest

DEFAULT_FEATURES = [
    "yoy_total_ghg_emissions_change",
    "yoy_energy_consumption_change",
    "yoy_water_consumption_change",
    "yoy_waste_generated_change",
    "emission_intensity",
    "energy_intensity",
    "water_intensity",
    "waste_intensity",
    "yoy_production_output_change",
    "yoy_revenue_change",
]


def run_isolation_forest(records, feature_names=None):
    feature_names = feature_names or DEFAULT_FEATURES
    matrix, usable = [], []
    for r in records:
        row = [r.get(f) for f in feature_names]
        if all(v is not None and np.isfinite(v) for v in row):
            matrix.append(row)
            usable.append(r)
    if len(matrix) < 8:
        return {"available": False, "reason": "Need at least 8 complete periodic observations for ML anomaly detection.", "results": []}
    X = np.asarray(matrix, float)
    model = IsolationForest(n_estimators=300, contamination="auto", random_state=42)
    labels = model.fit_predict(X)
    scores = -model.score_samples(X)
    results = []
    for r, label, score in zip(usable, labels, scores):
        results.append({"report_id": r["report_id"], "anomaly_label": "ANOMALY" if label == -1 else "NORMAL", "model_score": float(score), "model_version": "isolation-forest-v2-periodic", "feature_version": "features-v2-periodic"})
    return {"available": True, "results": results, "observations": len(usable), "feature_names": feature_names}
