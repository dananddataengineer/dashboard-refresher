import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://bi.apollohealthbridge.in"
MAIN_URL = "https://bi.apollohealthbridge.in/dashboards/"

def auto_refresh_all_dashboards():
    overall_start = time.time()

    with sync_playwright() as p:
        print("🚀 Launching cloud browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Open main dashboards page
        print(f"📌 Opening main page: {MAIN_URL}")
        main_start = time.time()
        page.goto(MAIN_URL, timeout=60000)
        time.sleep(5)
        print(f"   Main page loaded in {round(time.time() - main_start, 2)} seconds.")

        # Step 2: Discover all dashboard links
        links = page.locator("a[href*='/dashboards/']").all()
        found_urls = set()

        for link in links:
            href = link.get_attribute("href")
            if href:
                full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
                found_urls.add(full_url)

        urls_list = list(found_urls)
        if not urls_list:
            urls_list = [MAIN_URL]

        print(f"\n🔍 Found {len(urls_list)} dashboard(s) to refresh.\n" + "="*50)

        # Step 3: Visit each dashboard and measure exact loading time
        for idx, url in enumerate(urls_list, start=1):
            print(f"[{idx}/{len(urls_list)}] Refreshing: {url}")
            dash_start = time.time()
            
            try:
                page.goto(url, timeout=60000)
                time.sleep(10)  # Wait for charts/data to finish rendering
                
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ✓ Success | Title: {page.title()} | Time Taken: {time_taken}s")
            except Exception as e:
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ❌ Failed after {time_taken}s | Error: {e}")

        browser.close()
        total_time = round(time.time() - overall_start, 2)
        print("="*50 + f"\n🎉 All dashboards finished in {total_time} seconds total!")

if __name__ == "__main__":
    auto_refresh_all_dashboards()
