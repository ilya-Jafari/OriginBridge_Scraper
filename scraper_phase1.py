import asyncio
import json
import random
from playwright.async_api import async_playwright

# Die Liste deiner Produkte für OriginBridge
PRODUCT_LIST = [
    "Polyethylene PE", "Ammonium Phosphate", "Urea", 
    "Pet Coke Calcined", "Sulphur", "Paraffin Wax", 
    "Pistachio", "Apple Puree Concentrate"
]

async def scrape_product(page, product):
    print(f"🔍 Suche nach: {product}...")
    
    # Zur Suche navigieren
    await page.goto(f"https://www.europages.co.uk/companies/Search.html?q={product}")
    await page.wait_for_timeout(random.randint(2000, 4000)) # Zufällige Pause

    # Firmen finden (Überschriften h2)
    companies = await page.query_selector_all("h2")
    
    results = []
    for company in companies[:15]: # Die Top 15 pro Produkt
        name = await company.inner_text()
        if name.strip() and "Visable" not in name: # Filtert die Eigenwerbung von Europages aus
            results.append({
                "company_name": name.strip(),
                "category": product,
                "source": "Europages"
            })
    return results

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headless=True für Speed später
        page = await browser.new_page()
        
        # Einmalig Cookies akzeptieren
        await page.goto("https://www.europages.co.uk/")
        try:
            await page.get_by_role("button", name="ACCEPT ALL").click(timeout=5000)
        except:
            pass

        all_data = []

        for prod in PRODUCT_LIST:
            data = await scrape_product(page, prod)
            all_data.extend(data)
            print(f"✅ {len(data)} Firmen für {prod} gefunden.")
            
        # Speichern als JSON
        with open("suppliers_raw.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        
        print("\n🏆 Phase 1-A abgeschlossen! Datei 'suppliers_raw.json' wurde erstellt.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())