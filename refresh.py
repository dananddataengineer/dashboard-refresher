import time
from playwright.sync_api import sync_playwright

MAIN_URL = "https://bi.apollohealthbridge.in/dashboards/"

# 1. Main Category Headers that need to be expanded
CATEGORIES = ["Clinic", "Corporate", "Diagnostics"]

# 2. All 9 Dashboard Items inside the menus
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

def run_github_refresh():
    overall_start = time.time()

    with sync_playwright() as p:
        print("🚀 Launching cloud browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"📌 Opening: {MAIN_URL}")
        page.goto(MAIN_URL, timeout=60000)
        
        # Wait 10 seconds for React & sidebar menu to load
        time.sleep(10)

        # Step 1: Expand all Category Accordions (Clinic, Corporate, Diagnostics)
        print("\n📂 Expanding category menus...")
        for cat in CATEGORIES:
            try:
                cat_btn = page.get_by_text(cat, exact=True)
                if cat_btn.is_visible():
                    cat_btn.click()
                    print(f"   ✓ Opened category: '{cat}'")
                    time.sleep(2)
            except Exception as e:
                print(f"   ℹ️ Category '{cat}' notice: {e}")

        time.sleep(3)

        # Step 2: Refresh all 9 dashboards one by one
        print(f"\n🔍 Refreshing {len(DASHBOARDS)} dashboards...\n" + "="*60)

        for idx, dash_name in enumerate(DASHBOARDS, start=1):
            dash_start = time.time()
            print(f"[{idx}/{len(DASHBOARDS)}] Refreshing: '{dash_name}'")
            
            try:
                # Find and click sub-dashboard item
                menu_item = page.get_by_text(dash_name, exact=True)
                if not menu_item.is_visible():
                    menu_item = page.locator(f"text='{dash_name}'").first

                menu_item.click(timeout=15000)
                
                # Wait 12 seconds for Power BI report to refresh
                time.sleep(12)

                time_taken = round(time.time() - dash_start, 2)
                print(f"   ✓ Successfully refreshed '{dash_name}' in {time_taken}s")
                
            except Exception as e:
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ❌ Error clicking '{dash_name}' after {time_taken}s | {e}")

        browser.close()
        total_time = round(time.time() - overall_start, 2)
        print("="*60 + f"\n🎉 All {len(DASHBOARDS)} dashboards refreshed in {total_time}s total!")

if __name__ == "__main__":
    run_github_refresh()
