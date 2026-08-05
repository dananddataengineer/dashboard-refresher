import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://bi.apollohealthbridge.in"
MAIN_URL = "https://bi.apollohealthbridge.in/dashboards/"

def auto_refresh_all_dashboards():
    with sync_playwright() as p:
        print("Launching cloud browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Open the main dashboards page
        print(f"Opening main page: {MAIN_URL}")
        page.goto(MAIN_URL, timeout=60000)
        time.sleep(5)  # Wait 5 seconds for page links to render

        # 2. Auto-discover all dashboard links on the page
        links = page.locator("a[href*='/dashboards/']").all()
        found_urls = set()

        for link in links:
            href = link.get_attribute("href")
            if href:
                full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
                found_urls.add(full_url)

        urls_list = list(found_urls)
        
        # If no internal dashboard links found, default to main page
        if not urls_list:
            urls_list = [MAIN_URL]

        print(f"✓ Found {len(urls_list)} dashboard(s) to refresh!")

        # 3. Visit each discovered dashboard link
        for idx, url in enumerate(urls_list, start=1):
            print(f"[{idx}/{len(urls_list)}] Refreshing: {url}")
            try:
                page.goto(url, timeout=60000)
                time.sleep(10)  # Wait 10 seconds for charts and data to load
                print(f"  ✓ Refreshed successfully: {page.title()}")
            except Exception as e:
                print(f"  ❌ Error loading {url}: {e}")

        browser.close()
        print("🎉 Finished refreshing all dashboards!")

if __name__ == "__main__":
    auto_refresh_all_dashboards()
