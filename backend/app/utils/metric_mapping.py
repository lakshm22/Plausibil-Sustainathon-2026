ALIASES = {
    "scope_1_emissions": ["scope 1 ghg emissions", "scope-1 emissions", "direct ghg emissions", "scope 1 emissions"],
    "scope_2_emissions": ["scope 2 ghg emissions", "scope-2 emissions", "indirect ghg emissions", "scope 2 emissions"],
    "total_ghg_emissions": ["total ghg emissions", "total greenhouse gas emissions", "total emissions"],
    "energy_consumption": ["energy consumption", "total energy consumed", "energy consumed"],
    "water_withdrawal": ["water withdrawal", "water withdrawn"],
    "water_consumption": ["water consumption", "water consumed"],
    "waste_generated": ["waste generated", "total waste generated"],
    "production_output": ["production output", "production", "output"],
    "revenue": ["revenue", "turnover"],
    "emission_intensity": ["emission intensity", "ghg intensity"],
    "energy_intensity": ["energy intensity"],
    "water_intensity": ["water intensity"],
    "waste_intensity": ["waste intensity"],
}

def map_metric(name: str):
    cleaned = " ".join((name or "").lower().replace("_", " ").split())
    for canonical, aliases in ALIASES.items():
        if cleaned == canonical.replace("_", " ") or cleaned in aliases:
            return canonical
    return "AMBIGUOUS"
