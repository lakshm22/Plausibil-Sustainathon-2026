from collections import defaultdict

def build_features(rows):
    by_company = defaultdict(list)
    for r in rows:
        by_company[r["company_id"]].append(r)
    features = []
    for company_id, company_rows in by_company.items():
        company_rows.sort(key=lambda x: x["financial_year"])
        previous = {}
        for r in company_rows:
            current = r["metrics"]
            for metric in ["scope_1_emissions","scope_2_emissions","total_ghg_emissions","energy_consumption","water_consumption","waste_generated","production_output","revenue"]:
                value = current.get(metric)
                if value is not None and previous.get(metric) not in (None, 0):
                    features.append((r["report_id"], f"yoy_{metric}_change", (value/previous[metric]-1)*100))
            production = current.get("production_output")
            if production and production > 0:
                if current.get("total_ghg_emissions") is not None:
                    features.append((r["report_id"], "emission_intensity", current["total_ghg_emissions"]/production))
                if current.get("energy_consumption") is not None:
                    features.append((r["report_id"], "energy_intensity", current["energy_consumption"]/production))
                if current.get("water_consumption") is not None:
                    features.append((r["report_id"], "water_intensity", current["water_consumption"]/production))
                if current.get("waste_generated") is not None:
                    features.append((r["report_id"], "waste_intensity", current["waste_generated"]/production))
            previous = current.copy()
    return features
