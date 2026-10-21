from app.utils.unit_converter import convert

TARGETS = {
    "scope_1_emissions": "tCO2e",
    "scope_2_emissions": "tCO2e",
    "total_ghg_emissions": "tCO2e",
    "energy_consumption": "MWh",
    "water_withdrawal": "kL",
    "water_consumption": "kL",
    "waste_generated": "t",
}

def normalize_metric(item):
    metric = item["metric_name"]
    raw = item["raw_value"]
    unit = item["raw_unit"]
    target = TARGETS.get(metric)
    if raw is None or not target or not unit:
        item["normalized_value"] = None
        item["normalized_unit"] = target or ""
        if metric in TARGETS and not unit:
            item["data_quality_status"] = "LOW_CONFIDENCE"
        return item
    try:
        item["normalized_value"] = convert(raw, unit, target)
        item["normalized_unit"] = target
        item["data_quality_status"] = "NORMALIZED"
    except ValueError:
        item["normalized_value"] = None
        item["normalized_unit"] = target
        item["data_quality_status"] = "AMBIGUOUS"
    return item
