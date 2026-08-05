import os
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

def run_with_auth_session():
    overall_start = time.time()

    with sync_playwright() as p:
        print("🚀 Launching cloud browser...")
        browser = p.chromium.launch(headless=True)
        
        # Load your logged-in session state from auth.json
        if os.path.exists("auth.json"):
            context = browser.new_context(
                storage_state="auth.json",
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            print("✓ Loaded logged-in user session (Anand) from auth.json! Bypassing OTP screen.")
        else:
            print("❌ auth.json NOT found! Please upload auth.json to your GitHub repository.")
            return

        page = context.new_page()

        print(f"📌 Opening: {MAIN_URL}")
        page.goto(MAIN_URL, timeout=60000, wait_until="networkidle")
        time.sleep(10)

        # Refresh all 9 Power BI dashboards
        print(f"\n🔍 Refreshing {len(DASHBOARDS)} dashboards...\n" + "="*60)

        for idx, dash_name in enumerate(DASHBOARDS, start=1):
            dash_start = time.time()
            print(f"[{idx}/{len(DASHBOARDS)}] Refreshing: '{dash_name}'")
            
            try:
                menu_item = page.get_by_text(dash_name, exact=False).first
                menu_item.click(timeout=15000)
                
                # Wait 12 seconds for Power BI report to refresh
                time.sleep(12)

                time_taken = round(time.time() - dash_start, 2)
                print(f"   ✓ Successfully refreshed '{dash_name}' in {time_taken}s")
                
            except Exception as e:
                time_taken = round(time.time() - dash_start, 2)
                print(f"   ❌ Error on '{dash_name}' after {time_taken}s | {e}")

        browser.close()
        total_time = round(time.time() - overall_start, 2)
        print("="*60 + f"\n🎉 All 9 Power BI dashboards refreshed in {total_time}s total!")

if __name__ == "__main__":
    run_with_auth_session()
