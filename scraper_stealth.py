import asyncio
import json
import random
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Wir starten den Browser ganz normal
        browser = await p.chromium.launch(headless=False)
        
        # Wir setzen die "Tarnung" manuell über den Kontext
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="Europe/Berlin"
        )
        
        page = await context.new_page()

        # Wir tricksen ein paar Bot-Erkennungen manuell aus
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        print("🚀 OriginBridge Stealth-Scraper (Manual-Patch) startet...")

        # 1. Hauptseite aufrufen
        await page.goto("https://www.europages.co.uk/", wait_until="domcontentloaded")
        
        # GIB DIR ZEIT: Wenn ein Captcha kommt, hast du jetzt 10 Sekunden es zu lösen
        print("⏳ Pause... Falls ein 'Bist du ein Mensch?'-Check kommt, löse ihn jetzt im Browser!")
        await page.wait_for_timeout(8000)

        # 2. Cookies akzeptieren
        try:
            btn = page.get_by_role("button", name="ACCEPT ALL")
            if await btn.is_visible():
                await btn.click()
                print("✅ Cookies akzeptiert.")
        except: pass

        # 3. Suchwort eintippen (ganz langsam wie ein Mensch)
        try:
            search_input = page.get_by_placeholder("Search", exact=False)
            await search_input.click()
            # Wir tippen den Text Buchstabe für Buchstabe
            for char in "Polyethylene":
                await page.keyboard.type(char, delay=random.randint(100, 250))
                
            await page.keyboard.press("Enter")
            print("🔍 Suche mit 'Human-Typing' abgeschickt...")
        except:
            print("❌ Suchfeld nicht gefunden. Seite wurde evtl. blockiert.")
            await page.screenshot(path="error_view.png")
            return

        # 4. Warten und Ergebnisse checken
        await page.wait_for_timeout(5000)
        
        companies = await page.query_selector_all("h2")
        
        found_data = []
        for comp in companies[:10]:
            name = await comp.inner_text()
            if name.strip() and "Visable" not in name:
                print(f"🏢 Gefunden: {name.strip()}")
                found_data.append({"company": name.strip()})

        if found_data:
            with open("test_results.json", "w") as f:
                json.dump(found_data, f, indent=4)
            print(f"🏆 Erfolg! {len(found_data)} Firmen gespeichert.")
        else:
            print("⚠️ Keine Firmen gefunden. Prüfe 'check_this.png'.")
            await page.screenshot(path="check_this.png")

        await page.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())