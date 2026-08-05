from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("Opening Chrome... Please log in with your Email & OTP.")
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://bi.apollohealthbridge.in/dashboards/")

    print("Waiting for you to log in with Email & OTP...")
    # Waits up to 3 minutes for you to complete OTP login
    page.wait_for_selector("text='Doctor Performance'", timeout=180000)

    # Save session token
    context.storage_state(path="auth.json")
    print("\n🎉 SUCCESS! 'auth.json' file created successfully in your folder!")
    browser.close()