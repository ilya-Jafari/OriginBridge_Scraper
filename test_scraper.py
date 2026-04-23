import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Wir fügen einen User-Agent hinzu, damit wir wie ein echter Mac-User aussehen
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("🚀 OriginBridge Scraper startet...")
        
        # Die korrekte Such-URL für Europages (Englische Version ist oft stabiler für Scraper)
        search_query = "Polyethylene"
        url = f"https://www.europages.co.uk/companies/Search.html?q={search_query}"
        
        print(f"🔍 Navigiere zu: {url}")
        await page.goto(url)

        # SCHRITT 1: Cookie Banner wegklicken
        try:
            print("🍪 Versuche Cookie-Banner zu akzeptieren...")
            # Wir warten darauf, dass der "ACCEPT ALL" Button erscheint
            accept_button = page.get_by_role("button", name="ACCEPT ALL")
            await accept_button.wait_for(timeout=5000)
            await accept_button.click()
            print("✅ Cookies akzeptiert!")
        except Exception as e:
            print("ℹ️ Kein Cookie-Banner gefunden oder bereits weg.")

        # Kurz warten, bis die Liste lädt
        await page.wait_for_timeout(2000)

        # SCHRITT 2: Erfolg prüfen
        title = await page.title()
        print(f"✅ Seite geladen! Titel: {title}")

        # Wir machen einen neuen Screenshot
        await page.screenshot(path="suche_erfolg.png")
        print("📸 Neuer Screenshot 'suche_erfolg.png' erstellt.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())