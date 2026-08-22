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
    print("\n🚀 [START] 100% Accurate AppCreator24 Bot Running...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Login Page
            print("[1] Opening AppCreator24 Home...")
            page.goto("https://www.appcreator24.com/", wait_until="load", timeout=45000)
            time.sleep(2)

            print("[2] Entering Credentials...")
            email_box = page.locator('input[type="text"], input[type="email"]').first
            email_box.fill(EMAIL)

            pass_box = page.locator('input[type="password"]').first
            pass_box.fill(PASSWORD)
            time.sleep(1)

            print("[3] Clicking Sign in button...")
            page.locator('input[type="submit"], button:has-text("Sign in"), input[value*="Sign in"]').first.click()

            # 2. Wait for login redirect (Wait until dashboard loads)
            print("[4] Waiting for Dashboard Redirect...")
            page.wait_for_url(lambda url: "login" not in url.lower(), timeout=35000)
            time.sleep(4)  # Extra 4 seconds for full PHP redirect

            current_url = page.url
            print(f"[5] Successfully Landed on: {current_url}")

            # 3. Session ID Extraction (Multiple Sources)
            session_id = None
            
            # Method A: From URL
            match = re.search(r'idsesion=([a-zA-Z0-9]+)', current_url)
            if match:
                session_id = match.group(1)
            
            # Method B: From Links on Dashboard Page
            if not session_id:
                content = page.content()
                match = re.search(r'idsesion=([a-zA-Z0-9]+)', content)
                if match:
                    session_id = match.group(1)

            if not session_id:
                page.screenshot(path="error_screenshot.png")
                raise Exception("Login ho gaya par session ID detect nahi hua. Screenshot captured.")

            print(f"🔑 [6] Session ID Captured Successfully: {session_id}")

            # 4. Jump Directly to Notifications Page (pag=21)
            notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={session_id}&pag=21&idapp={APP_ID}"
            print(f"[7] Navigating directly to Notification Panel (App ID: {APP_ID})...")
            page.goto(notif_url, wait_until="load", timeout=35000)
            time.sleep(3)

            # 5. Click "New message"
            print("[8] Opening 'New message' form...")
            new_msg_btn = page.locator('input[value="New message"], a:has-text("New message")')
            new_msg_btn.first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 6. Fill Title & Subtitle
            print(f"[9] Filling Details -> Title: '{NOTIF_TITLE}' | Subtitle: '{NOTIF_MESSAGE}'...")
            inputs = page.locator('input[type="text"]')
            inputs.nth(0).fill(NOTIF_TITLE)
            inputs.nth(1).fill(NOTIF_MESSAGE)

            # 7. Click Next >>
            print("[10] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 8. Click Send >>
            print("[11] Confirming & Broadcasting Notification (Send >>)...")
            page.locator('input[value="Send >>"], input[value*="Send"]').first.click()
            time.sleep(6)

            print("\n" + "="*60)
            print("🎉🎉 100% SUCCESS: NOTIFICATION SENT TO ALL USERS! 🎉🎉")
            print("="*60 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
