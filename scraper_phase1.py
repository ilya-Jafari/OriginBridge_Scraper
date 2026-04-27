import asyncio
import json
import random
from playwright.async_api import async_playwright

PRODUCT_LIST = ["Polyethylene PE", "Urea", "Sulphur"] # Erstmal klein zum Testen

async def scrape_supplier_details(page, profile_url):
    """Besucht die Profilseite einer Firma und sammelt alles ein."""
    try:
        await page.goto(profile_url)
        await page.wait_for_timeout(random.randint(1000, 2000))
        
        # Wir holen uns den gesamten sichtbaren Text der Seite
        # Die KI wird später daraus ISO, Adresse und Website extrahieren
        content = await page.evaluate("() => document.body.innerText")
        
        # Wir versuchen, die Website-URL direkt zu finden, falls vorhanden
        website_element = await page.query_selector("a[href*='http']")
        website = await website_element.get_attribute("href") if website_element else "N/A"
        
        return {
            "raw_text": content[:2000], # Die ersten 2000 Zeichen reichen meistens
            "supplier_website": website
        }
    except:
        return {"raw_text": "Error loading details", "supplier_website": "N/A"}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://www.europages.co.uk/")
        try:
            await page.get_by_role("button", name="ACCEPT ALL").click(timeout=5000)
        except: pass

        all_suppliers = []

        for prod in PRODUCT_LIST:
            print(f"🔍 Suche läuft für: {prod}")
            await page.goto(f"https://www.europages.co.uk/companies/Search.html?q={prod}")
            await page.wait_for_timeout(3000)

            # Wir suchen die Links zu den Firmenprofilen
            links = await page.query_selector_all("a.company-name")
            
            # Wir nehmen die ersten 5 Firmen pro Produkt zum Testen (Deep Scraping dauert länger)
            profile_urls = []
            for link in links[:5]:
                href = await link.get_attribute("href")
                if href:
                    profile_urls.append("https://www.europages.co.uk" + href)

            for url in profile_urls:
                print(f"  📄 Extrahiere Details von: {url}")
                details = await scrape_supplier_details(page, url)
                
                all_suppliers.append({
                    "product": prod,
                    "profile_url": url,
                    "details": details["raw_text"],
                    "website": details["supplier_website"]
                })

        # Speichern der "rohen" Daten für die KI
        with open("deep_suppliers_raw.json", "w", encoding="utf-8") as f:
            json.dump(all_suppliers, f, ensure_ascii=False, indent=4)
        
        print("\n✅ Deep Scraping abgeschlossen! Datei 'deep_suppliers_raw.json' bereit.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())