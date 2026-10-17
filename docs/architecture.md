# Plausibil architecture

The prototype follows:

PDF -> extraction -> normalization -> structured metrics -> feature engineering -> rules/peers/ML -> flags -> evidence -> UI.

The numeric path is deterministic. The optional model path is explicitly separated from extraction confidence and rule evidence.

## Extension points

- Add table-aware BRSR parsers in `metric_extractor.py`.
- Add OCR rendering and Tesseract in `ocr_service.py`.
- Add persisted feature/model tables if training data grows.
- Add real SHAP TreeExplainer for a persisted Isolation Forest.
- Add report-to-report boundary text comparison.
- Add sector-specific peer groups and minimum peer counts.
