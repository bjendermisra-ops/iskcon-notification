import sys
import time
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_NAME = "Iskcon Padyatra"          # App Name

NOTIF_TITLE = "Hare Krishna"          # Title
NOTIF_MESSAGE = "Ekadashi fast reminder!"  # Message

def run():
    print("\n🚀 [START] Final AppCreator24 Bot Running...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Open Login
            print("[1] Opening AppCreator24...")
            page.goto("https://www.appcreator24.com/", timeout=45000)
            page.wait_for_selector('input[type="password"]', timeout=20000)

            # 2. Enter Credentials
            print("[2] Entering Credentials...")
            page.locator('input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            time.sleep(1)

            # 3. Sign In
            print("[3] Clicking Sign in...")
            page.locator('input[value="Sign in"], input[type="submit"], button:has-text("Sign in")').first.click()
            
            # Wait for login page to load (android-creator.php or intra.php)
            page.wait_for_selector('text="Apps", a[href*="idapp"], table', timeout=30000)
            print(f"✅ [4] Logged In! Current URL: {page.url}")
            time.sleep(2)

            # 4. Click on App Name (Iskcon Padyatra)
            print(f"[5] Clicking on '{APP_NAME}'...")
            page.locator(f'text="{APP_NAME}"').first.click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # 5. Click "Send notifications" in left sidebar
            print("[6] Opening 'Send notifications'...")
            page.locator('text="Send notifications"').first.click()
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # 6. Click "New message"
            print("[7] Clicking 'New message' button...")
            page.locator('input[value="New message"]').first.click()
            page.wait_for_selector('input[value="Next >>"], input[value*="Next"]', timeout=25000)
            time.sleep(1)

            # 7. Fill Title & Message
            print(f"[8] Filling Title: '{NOTIF_TITLE}' & Subtitle: '{NOTIF_MESSAGE}'...")
            text_inputs = page.locator('input[type="text"]')
            text_inputs.nth(0).fill(NOTIF_TITLE)
            text_inputs.nth(1).fill(NOTIF_MESSAGE)

            # 8. Click Next >>
            print("[9] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_selector('input[value="Send >>"], input[value*="Send"]', timeout=25000)
            time.sleep(1)

            # 9. Click Send >>
            print("[10] Confirming & Broadcasting (Send >>)...")
            page.locator('input[value="Send >>"], input[value*="Send"]').first.click()
            time.sleep(6)

            print("\n" + "="*55)
            print("🎉🎉 100% SUCCESS: NOTIFICATION DELIVERED! 🎉🎉")
            print("="*55 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
