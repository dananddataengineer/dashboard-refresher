import time
from playwright.sync_api import sync_playwright

MAIN_URL = "https://bi.apollohealthbridge.in/dashboards/"

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

def debug_and_refresh():
    overall_start = time.time()

    with sync_playwright() as p:
        print("🚀 Launching cloud browser in Full HD Desktop mode (1920x1080)...")
        
        # 1. Open browser in 1920x1080 resolution with a standard Chrome User-Agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"📌 Opening: {MAIN_URL}")
        page.goto(MAIN_URL, timeout=60000, wait_until="networkidle")
        time.sleep(8)

        # 2. Print Page Diagnostics to logs
        print(f"📄 Page Title: '{page.title()}'")
        print(f"🔗 Current URL: '{page.url}'")
        
        body_text = page.inner_text("body")
        print(f"📝 Page Text Preview:\n{body_text[:400]}\n" + "-"*50)

        # 3. Click Hamburger Menu icon (☰) if sidebar is collapsed
        try:
            # Try clicking top-left menu icon if present
            menu_icon = page.locator("button, svg, i, .sidebar-toggle, [aria-label*='menu' i]").first
            if menu_icon.is_visible():
                menu_icon.click()
                print("☰ Clicked top-left menu icon to expand sidebar.")
                time.sleep(3)
        except Exception as e:
            print(f"Notice on menu icon: {e}")

        # 4. Refresh all 9 Power BI dashboards
        print(f"\n🔍 Refreshing {len(DASHBOARDS)} dashboards...\n" + "="*60)

        for idx, dash_name in enumerate(DASHBOARDS, start=1):
            dash_start = time.time()
            print(f"[{idx}/{len(DASHBOARDS)}] Refreshing: '{dash_name}'")
            
            try:
                # Find menu item by text
                menu_item = page.get_by_text(dash_name, exact=False).first
                menu_item.click(timeout=15000)
                
                # Wait 12 seconds for Power BI charts to refresh
                time.sleep(12)

                time_taken = round(time.time() - dash_start, 2)
                print(f"   ✓ Successfully refreshed '{dash_name}' in {time_taken}s")
                
            except Exception as e:
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ❌ Error on '{dash_name}' after {time_taken}s | {e}")

        browser.close()
        total_time = round(time.time() - overall_start, 2)
        print("="*60 + f"\n🎉 Finished in {total_time}s total!")

if __name__ == "__main__":
    debug_and_refresh()
