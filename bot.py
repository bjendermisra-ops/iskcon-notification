import sys
import time
import re
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_ID = "4050991"                     # Iskcon Padyatra App ID

NOTIF_TITLE = "Hare Krishna"           # Title
NOTIF_MESSAGE = "Ekadashi fast reminder!"   # Message

def run():
    print("\n🚀 [START] Ultra-Reliable AppCreator24 Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Login Page
            print("[1] Opening AppCreator24...")
            page.goto("https://www.appcreator24.com/", wait_until="load", timeout=45000)
            time.sleep(2)

            print("[2] Filling Email & Password...")
            # Email input
            email_box = page.locator('input[type="text"], input[type="email"]').first
            email_box.click()
            email_box.fill("")
            email_box.type(EMAIL, delay=50)

            # Password input
            pass_box = page.locator('input[type="password"]').first
            pass_box.click()
            pass_box.fill("")
            pass_box.type(PASSWORD, delay=50)
            time.sleep(1)

            print("[3] Submitting Form via Enter / Click...")
            # Enter dabakar aur Sign In par click karke submit
            with page.expect_navigation(timeout=30000, wait_until="domcontentloaded"):
                pass_box.press("Enter")

            time.sleep(3)
            current_url = page.url
            print(f"[4] Current URL: {current_url}")

            # Session ID nikalna
            match = re.search(r'idsesion=([a-zA-Z0-9]+)', current_url)
            if not match:
                # Agar direct URL me nahi to page content se nikaalo
                content = page.content()
                match = re.search(r'idsesion=([a-zA-Z0-9]+)', content)

            if not match:
                page.screenshot(path="error_screenshot.png")
                raise Exception("लॉगिन असफल रहा! कृपया चेक करें कि पासवर्ड 'santosh@29' सही है?")

            session_id = match.group(1)
            print(f"🔑 [5] Session ID Captured: {session_id}")

            # 2. Jump directly to Send Notifications Page
            notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={session_id}&pag=21&idapp={APP_ID}"
            print(f"[6] Opening Notifications Page (App ID: {APP_ID})...")
            page.goto(notif_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)

            # 3. Click New Message
            print("[7] Clicking 'New message'...")
            page.locator('input[value="New message"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 4. Fill Title & Subtitle
            print(f"[8] Filling Title: '{NOTIF_TITLE}' & Subtitle: '{NOTIF_MESSAGE}'...")
            inputs = page.locator('input[type="text"]')
            inputs.nth(0).fill(NOTIF_TITLE)
            inputs.nth(1).fill(NOTIF_MESSAGE)

            # 5. Click Next >>
            print("[9] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 6. Click Send >>
            print("[10] Confirming Broadcast (Send >>)...")
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
