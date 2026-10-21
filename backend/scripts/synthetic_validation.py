from app.services.validation_engine import validate_total, validate_intensity, validate_yoy

def main():
    base={"scope_1_emissions":6500,"scope_2_emissions":3500,"total_ghg_emissions":10000,"production_output":100000,"emission_intensity":0.10}
    perturbations=[
        ("broken total", {**base,"total_ghg_emissions":13000}),
        ("wrong intensity", {**base,"emission_intensity":1.0}),
        ("large yoy", {**base}),
    ]
    for name,row in perturbations:
        print(name, validate_total(row), validate_intensity(row))
    print("Synthetic anomaly detection validation only; no real-world accuracy is claimed.")

if __name__=="__main__":
    main()
