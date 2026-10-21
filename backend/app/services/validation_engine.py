def pct_change(new, old):
    if old in (None, 0) or new is None:
        return None
    return (new / old - 1) * 100

def validate_total(metrics, tolerance_pct=2.0):
    s1, s2, total = metrics.get("scope_1_emissions"), metrics.get("scope_2_emissions"), metrics.get("total_ghg_emissions")
    if None in (s1, s2, total) or total == 0:
        return None
    diff_pct = abs((s1+s2-total)/total)*100
    if diff_pct > tolerance_pct:
        return {
            "flag_type":"INTERNAL_TOTAL_MISMATCH",
            "severity":"HIGH PRIORITY",
            "score":min(100, diff_pct),
            "title":"Scope 1 + Scope 2 does not reconcile to reported total",
            "description":f"Components sum to {s1+s2:.2f} tCO2e while the reported total is {total:.2f} tCO2e, a {diff_pct:.1f}% difference."
        }

def validate_intensity(metrics):
    production = metrics.get("production_output")
    emissions = metrics.get("total_ghg_emissions")
    reported = metrics.get("emission_intensity")
    if production in (None, 0) or emissions is None or reported is None:
        return None
    calculated = emissions/production
    if calculated == 0:
        return None
    delta = abs((reported-calculated)/calculated)*100
    if delta > 5:
        return {
            "flag_type":"INTENSITY_MISMATCH",
            "severity":"HIGH PRIORITY",
            "score":min(100, delta),
            "title":"Reported emission intensity differs from calculated intensity",
            "description":f"Reported intensity is {reported:.4f}; calculated intensity is {calculated:.4f}, a {delta:.1f}% difference."
        }

def validate_yoy(metrics, previous, threshold_pct=50):
    flags=[]
    for metric in ["scope_1_emissions","scope_2_emissions","total_ghg_emissions","energy_consumption","water_consumption","waste_generated"]:
        change=pct_change(metrics.get(metric), previous.get(metric))
        if change is not None and abs(change) >= threshold_pct:
            flags.append({
                "flag_type":"LARGE_YOY_MOVEMENT",
                "severity":"REVIEW" if abs(change)<100 else "HIGH PRIORITY",
                "score":abs(change),
                "title":f"Large year-on-year movement in {metric.replace('_',' ')}",
                "description":f"The metric changed by {change:+.1f}% versus the previous available year. Large movements can have legitimate operational or boundary explanations and warrant source review."
            })
    return flags
