import sys
import time
import re
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_ID = "4050991"                     # Iskcon Padyatra

NOTIF_TITLE = "Hare Krishna"           # Title
NOTIF_MESSAGE = "Ekadashi fast reminder!"   # Message

def run():
    print("\n🚀 [START] 100% Bulletproof AppCreator24 Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Open AppCreator24
            print("[1] Opening AppCreator24...")
            page.goto("https://www.appcreator24.com/", timeout=45000)
            page.wait_for_selector('input[type="password"]', timeout=20000)

            # 2. Fill Login Details
            print("[2] Entering Email & Password...")
            page.locator('input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            time.sleep(1)

            # 3. Click Sign in and WAIT FOR intra.php (Dashboard)
            print("[3] Clicking Sign In and waiting for Dashboard (intra.php)...")
            with page.expect_navigation(url=re.compile(r".*intra\.php.*"), timeout=35000):
                page.locator('input[value="Sign in"], input[type="submit"], button:has-text("Sign in")').first.click()

            dashboard_url = page.url
            print(f"✅ [4] Logged In! Landed on: {dashboard_url}")

            # 4. Extract Session ID
            match = re.search(r'idsesion=([a-zA-Z0-9]+)', dashboard_url)
            if not match:
                raise Exception(f"Session ID URL me nahi mila: {dashboard_url}")
            
            session_id = match.group(1)
            print(f"🔑 [5] Session ID Captured: {session_id}")

            # 5. Jump Directly to Notifications Page
            notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={session_id}&pag=21&idapp={APP_ID}"
            print(f"[6] Jumping directly to Notifications Page for App ID: {APP_ID}...")
            page.goto(notif_url, timeout=30000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # 6. Click "New message"
            print("[7] Clicking 'New message' button...")
            page.locator('input[value="New message"]').first.click()
            page.wait_for_selector('input[value="Next >>"], input[value*="Next"]', timeout=25000)
            time.sleep(1)

            # 7. Fill Title & Message
            print(f"[8] Filling Title: '{NOTIF_TITLE}' & Message: '{NOTIF_MESSAGE}'...")
            text_inputs = page.locator('input[type="text"]')
            text_inputs.nth(0).fill(NOTIF_TITLE)
            text_inputs.nth(1).fill(NOTIF_MESSAGE)

            # 8. Click Next >>
            print("[9] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_selector('input[value="Send >>"], input[value*="Send"]', timeout=25000)
            time.sleep(1)

            # 9. Click Send >>
            print("[10] Clicking 'Send >>'...")
            page.locator('input[value="Send >>"], input[value*="Send"]').first.click()
            time.sleep(5)

            print("\n" + "="*55)
            print("🎉🎉 100% SUCCESS: NOTIFICATION SENT LIVE! 🎉🎉")
            print("="*55 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
