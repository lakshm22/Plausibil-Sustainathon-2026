import re
from app.utils.metric_mapping import map_metric

NUMBER = r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"

PATTERNS = {
    "scope_1_emissions": rf"scope[\s-]*1[^\n]{{0,100}}?({NUMBER})\s*(kgCO2e|tCO2e|tonnes?|kg)?",
    "scope_2_emissions": rf"scope[\s-]*2[^\n]{{0,100}}?({NUMBER})\s*(kgCO2e|tCO2e|tonnes?|kg)?",
    "total_ghg_emissions": rf"total[^\n]{{0,80}}?(?:ghg|greenhouse)[^\n]{{0,80}}?({NUMBER})\s*(kgCO2e|tCO2e|tonnes?|kg)?",
    "energy_consumption": rf"energy[^\n]{{0,80}}?(?:consumption|consumed)[^\n]{{0,80}}?({NUMBER})\s*(kWh|MWh|GWh)?",
    "water_consumption": rf"water[^\n]{{0,80}}?(?:consumption|consumed)[^\n]{{0,80}}?({NUMBER})\s*(litres?|kL|ML)?",
    "water_withdrawal": rf"water[^\n]{{0,80}}?withdraw(?:al|n)[^\n]{{0,80}}?({NUMBER})\s*(litres?|kL|ML)?",
    "waste_generated": rf"waste[^\n]{{0,80}}?generated[^\n]{{0,80}}?({NUMBER})\s*(kg|tonnes?|t)?",
    "production_output": rf"production[^\n]{{0,80}}?(?:output)?[^\n]{{0,80}}?({NUMBER})\s*(tonnes?|t|units?)?",
    "revenue": rf"revenue[^\n]{{0,50}}?({NUMBER})",
}

def extract_metrics(pages):
    results = []
    for p in pages:
        text = p["text"]
        for metric, pattern in PATTERNS.items():
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                value = float(m.group(1).replace(",", ""))
                unit = (m.group(2) or "").strip()
                results.append({
                    "metric_name": map_metric(metric),
                    "raw_value": value,
                    "raw_unit": unit,
                    "page_number": p["page_number"],
                    "table_reference": "Text extraction",
                    "source_text": text[max(0, m.start()-120):min(len(text), m.end()+120)],
                    "extraction_confidence": 0.72,
                    "data_quality_status": "VALID",
                })
    return results
