"""Real browser smoke tests for bilingual static preview, not a substitute for owner visual signoff."""
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = (Path(__file__).resolve().parent / "site" / "index.html").as_uri()

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for viewport in ({"width": 390, "height": 844}, {"width": 1366, "height": 768}):
            page = browser.new_page(viewport=viewport)
            errors = []
            page.on("pageerror", lambda err: errors.append(str(err)))
            page.goto(SITE)
            assert page.locator("html").get_attribute("lang") in ("en", "ar")
            assert page.locator("#main").count() == 1
            assert page.locator("#language-select").count() == 1
            page.locator("#language-select").select_option("ar")
            assert page.locator("html").get_attribute("dir") == "rtl"
            assert page.locator("html").get_attribute("lang") == "ar"
            page.reload()
            assert page.locator("html").get_attribute("dir") == "rtl"
            page.locator("#language-select").select_option("en")
            assert page.locator("html").get_attribute("dir") == "ltr"
            assert page.locator("html").get_attribute("lang") == "en"
            assert not errors, errors
            page.close()
        browser.close()
    print("PASS: Chromium RTL/LTR, language persistence, desktop/mobile and JS runtime smoke checks")

if __name__ == "__main__":
    main()
