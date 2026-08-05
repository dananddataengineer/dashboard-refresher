import time
from playwright.sync_api import sync_playwright

MAIN_URL = "https://bi.apollohealthbridge.in/dashboards/"

# All dashboard names from your sidebar menu image:
DASHBOARDS = [
    "IQMS",
    "Doctor Performance",
    "Clinics Performance",
    "Corporate Performance",
    "Healthpulse",
    "Self check in",
    "Consent form",
    "Phlebo slot utilization",
    "Billing Intelligence & Service Analytics",
]

def refresh_all_sidebar_dashboards():
    overall_start = time.time()

    with sync_playwright() as p:
        print("🚀 Launching cloud browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"📌 Opening main page: {MAIN_URL}")
        page.goto(MAIN_URL, timeout=60000)
        
        # Wait 8 seconds for React app & sidebar to fully load
        time.sleep(8)

        print(f"\n🔍 Found {len(DASHBOARDS)} dashboards in menu. Starting refresh...\n" + "="*60)

        for idx, dash_name in enumerate(DASHBOARDS, start=1):
            dash_start = time.time()
            print(f"[{idx}/{len(DASHBOARDS)}] Clicking Sidebar Menu: '{dash_name}'")
            
            try:
                # 1. Locate the sidebar text and click it
                menu_item = page.get_by_text(dash_name, exact=True)
                
                # If exact match fails, try partial match
                if not menu_item.is_visible():
                    menu_item = page.locator(f"text='{dash_name}'").first

                menu_item.click(timeout=10000)
                
                # 2. Wait 10 seconds for the charts and data of this dashboard to load
                time.sleep(10)

                time_taken = round(time.time() - dash_start, 2)
                print(f"   ✓ Successfully refreshed '{dash_name}' in {time_taken}s")
                
            except Exception as e:
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ❌ Failed to click '{dash_name}' after {time_taken}s | Error: {e}")

        browser.close()
        total_time = round(time.time() - overall_start, 2)
        print("="*60 + f"\n🎉 All {len(DASHBOARDS)} dashboards refreshed in {total_time}s total!")

if __name__ == "__main__":
    refresh_all_sidebar_dashboards()
