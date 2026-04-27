import asyncio
import os
import requests
from playwright.async_api import async_playwright

# Erweiterte Seed-Liste mit spezifischeren Produkten
SEED_DATA = [
    {"company": "SABIC", "products": ["HDPE", "LDPE", "LLDPE", "Polypropylene"]},
    {"company": "Yara", "products": ["Urea 46%", "Ammonium Nitrate", "Technical Grade Urea"]},
    {"company": "OCP Group", "products": ["DAP", "MAP", "Phosphoric Acid"]}
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        for item in SEED_DATA:
            for product in item["products"]:
                search_query = f'"{item["company"]}" "{product}" technical data sheet filetype:pdf'
                url = f"https://www.bing.com/search?q={search_query.replace(' ', '+')}"
                
                print(f"\n--- 🔎 Suche: {item['company']} - {product} ---")
                await page.goto(url)
                
                # Hier hast du Zeit für das Captcha
                print("⏳ Checke die Seite... Falls ein Captcha kommt, löse es.")
                print("👉 Drücke ENTER im Terminal, wenn die Ergebnisse da sind (oder 's' zum Überspringen)...")
                user_input = await asyncio.to_thread(input)
                if user_input.lower() == 's': continue

                # Wir suchen alle Links, die "pdf" im Text oder in der URL haben
                links = await page.query_selector_all("a")
                pdf_urls = []
                
                for link in links:
                    href = await link.get_attribute("href")
                    if href and (".pdf" in href.lower() or "download" in href.lower()):
                        if href.startswith("http") and href not in pdf_urls:
                            pdf_urls.append(href)

                print(f"✅ {len(pdf_urls)} potenzielle PDFs gefunden.")

                # Die besten 3 PDFs pro Unterprodukt herunterladen
                for i, target_url in enumerate(pdf_urls[:3]):
                    try:
                        print(f"  📥 Downloade PDF {i+1}...")
                        response = requests.get(target_url, timeout=10)
                        clean_name = f"{item['company']}_{product}_{i}".replace(" ", "_").replace("/", "-")
                        with open(f"downloads/{clean_name}.pdf", 'wb') as f:
                            f.write(response.content)
                    except Exception as e:
                        print(f"  ❌ Download fehlgeschlagen: {e}")

        print("\n🏆 Massen-Download beendet! Schau in deinen 'downloads' Ordner.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())