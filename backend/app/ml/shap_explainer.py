def explain_isolation_forest(_model, feature_names, row):
    # Kept dependency-light for the demo. Replace with TreeExplainer/model output
    # when the trained model object is persisted.
    ranked = sorted(
        [(name, abs(float(value))) for name, value in zip(feature_names, row) if value is not None],
        key=lambda x: x[1],
        reverse=True,
    )
    return [{"feature": name, "contribution": round(value, 4)} for name, value in ranked[:5]]
