def evidence_payload(flag, metrics):
    return {
        "flag_id": flag.id,
        "evidence": [
            {
                "metric": m.metric_name,
                "raw_value": m.raw_value,
                "raw_unit": m.raw_unit,
                "normalized_value": m.normalized_value,
                "normalized_unit": m.normalized_unit,
                "page_number": m.page_number,
                "table_reference": m.table_reference,
                "source_text": m.source_text,
                "extraction_confidence": m.extraction_confidence,
            } for m in metrics
        ],
    }
