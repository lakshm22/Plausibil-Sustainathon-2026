CONVERSIONS = {
    ("kg", "t"): 0.001,
    ("kgco2e", "tco2e"): 0.001,
    ("kwh", "mwh"): 0.001,
    ("gwh", "mwh"): 1000.0,
    ("litres", "kl"): 0.001,
    ("liters", "kl"): 0.001,
    ("ml", "kl"): 1.0,
}

def normalize_unit(unit: str):
    u = (unit or "").strip().lower().replace(" ", "")
    aliases = {
        "kgco2-e": "kgco2e",
        "kgco2eq": "kgco2e",
        "tco2-e": "tco2e",
        "tco2eq": "tco2e",
        "tonnes": "t",
        "tonne": "t",
        "mwh": "mwh",
        "kwh": "kwh",
        "gwh": "gwh",
        "litre": "litres",
        "liter": "liters",
    }
    return aliases.get(u, u)

def convert(value: float, raw_unit: str, target_unit: str):
    ru = normalize_unit(raw_unit)
    tu = normalize_unit(target_unit)
    if ru == tu:
        return value
    factor = CONVERSIONS.get((ru, tu))
    if factor is None:
        raise ValueError(f"Unknown or ambiguous conversion: {raw_unit} -> {target_unit}")
    return value * factor
