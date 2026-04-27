import asyncio
import json
import random
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("🚀 Debug-Modus: Fenster wird NICHT automatisch geschlossen.")

        await page.goto("https://www.europages.co.uk/", wait_until="domcontentloaded")
        
        # Cookie Banner
        try:
            await page.get_by_role("button", name="ACCEPT ALL").click(timeout=3000)
        except: pass

        # Tippen
        search_input = page.get_by_placeholder("Search", exact=False)
        await search_input.click()
        for char in "Polyethylene":
            await page.keyboard.type(char, delay=100)
        await page.keyboard.press("Enter")
        
        print("🔍 Suche läuft... bitte warten.")
        
        # Wir warten darauf, dass die URL sich ändert oder Ergebnisse laden
        await page.wait_for_timeout(5000)

        # DEBUG: Wir schauen uns an, was wirklich auf der Seite ist
        # Wir suchen nach allen Links, die das Wort 'companies' in der URL haben
        links = await page.query_selector_all("a")
        
        found_data = []
        for link in links:
            href = await link.get_attribute("href")
            text = await link.inner_text()
            
            # Europages Firmenlinks enthalten meistens "/companies/"
            if href and "/companies/" in href and text.strip():
                if len(text.strip()) > 3: # Kurze Texte wie "More" ignorieren
                    print(f"🏢 Firma gefunden: {text.strip()}")
                    found_data.append({"name": text.strip(), "url": href})

        if not found_data:
            print("⚠️ Immer noch nichts gefunden. Schau jetzt in das Browserfenster!")
            print("Steht dort 'No results' oder ein Captcha?")
        else:
            print(f"🏆 Erfolg! {len(found_data)} potenzielle Firmen gefunden.")

        # DAS HÄLT DAS FENSTER OFFEN
        print("\n👉 Schau dir das Browser-Fenster an. Wenn du fertig bist, drücke ENTER im Terminal, um es zu schließen.")
        await asyncio.to_thread(input) 
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())