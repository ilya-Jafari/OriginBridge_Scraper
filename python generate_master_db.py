import json
import random

def generate_master_db():
    sectors = {
        "Polymers": ["Polyethylene PE", "Paraffin Wax", "Pet Coke Calcined"],
        "Chemicals": ["Urea", "Ammonium Phosphate", "Sulphur"],
        "Agro": ["Pistachio", "Apple Puree Concentrate", "Tomato Paste"]
    }
    
    countries = [
        ("USA", "Houston", "Oakland"), ("China", "Shanghai", "Dalian"), 
        ("Germany", "Hamburg", "Bremerhaven"), ("UAE", "Jebel Ali", "Ruwais"),
        ("Saudi Arabia", "Jubail", "Yanbu"), ("Brazil", "Santos", "Paranagua"),
        ("Egypt", "Alexandria", "Damietta"), ("Vietnam", "Haiphong", "Ho Chi Minh")
    ]

    certifications = ["ISO 9001", "ISO 14001", "HACCP", "BRC", "GMP", "REACH"]
    incoterms = ["FOB", "CIF", "DDP", "EXW"]

    db = []

    for i in range(1, 101):
        sector = random.choice(list(sectors.keys()))
        product = random.choice(sectors[sector])
        country, hub1, hub2 = random.choice(countries)
        
        # Technische Specs je nach Sektor
        tech_specs = {}
        if sector == "Agro":
            tech_specs = {
                "purity_brix": f"{random.randint(28, 38)}%",
                "ph_value": round(random.uniform(4.0, 4.8), 2),
                "shelf_life": "24 Months"
            }
        elif sector == "Chemicals":
            tech_specs = {
                "purity": f"{random.uniform(99.1, 99.9):.2f}%",
                "moisture": f"{random.uniform(0.1, 0.5):.2f}%",
                "grade": "Technical/Food Grade"
            }
        else: # Polymers
            tech_specs = {
                "density": f"{random.randint(910, 960)} kg/m³",
                "melt_flow_rate": f"{random.uniform(0.1, 20.0):.1f} g/10min",
                "viscosity": "High/Medium"
            }

        entry = {
            "id": f"OB-{sector[:3].upper()}-{i:03d}",
            "company_name": f"{product.split()[0]} Global {i}",
            "sector": sector,
            "product": product,
            "location": {
                "city": f"Industrial City {i}",
                "country": country
            },
            "export_hub": random.choice([hub1, hub2]),
            "technical_specs": tech_specs,
            "certifications": random.sample(certifications, k=random.randint(1, 3)),
            "logistics": {
                "incoterms": random.choice(incoterms),
                "packaging": random.choice(["25kg Bags", "Big Bags 1000kg", "Aseptic Drums", "Bulk"]),
                "min_order_quantity": f"{random.randint(20, 100)} Tons"
            },
            "estimated_capacity_yearly": f"{random.randint(50000, 1000000)} Tons"
        }
        db.append(entry)

    with open("originbridge_master_db.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Master-Datei mit {len(db)} Einträgen erstellt!")

if __name__ == "__main__":
    generate_master_db()