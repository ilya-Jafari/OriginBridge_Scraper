import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Wir schauen zu!
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        print("🚀 OriginBridge Scraper Phase 3 startet...")
        
        # 1. Hauptseite aufrufen
        await page.goto("https://www.europages.co.uk/")

        # 2. Cookie Banner akzeptieren
        try:
            await page.get_by_role("button", name="ACCEPT ALL").click(timeout=5000)
            print("✅ Cookies weg.")
        except:
            print("ℹ️ Kein Banner.")

        # 3. Suchwort eintippen
        search_box = page.get_by_placeholder("Search") # Das Suchfeld finden
        await search_box.fill("Polyethylene")
        await search_box.press("Enter")
        
        print("🔍 Suche läuft...")
        await page.wait_for_load_state("networkidle") # Warten bis alles geladen ist

        # 4. Die Firmen-Karten finden
        # Wir suchen nach den Überschriften der Firmen (meistens h2 oder h3)
        await page.wait_for_selector("h2")
        
        # Wir holen alle Firmennamen auf der Seite
        companies = await page.query_selector_all("h2")
        
        print("\n--- GEFUNDENE SUPPLIER ---")
        for i, company in enumerate(companies[:10]): # Die ersten 10
            name = await company.inner_text()
            if name.strip():
                print(f"{i+1}. Firma: {name.strip()}")

        # Screenshot zur Kontrolle
        await page.screenshot(path="polyethylene_ergebnis.png")
        print("\n📸 Check 'polyethylene_ergebnis.png' für die echte Liste.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())