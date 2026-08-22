import sys
import time
import re
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_ID = "4050991"                     # आपका Iskcon Padyatra ऐप ID

NOTIF_TITLE = "Hare Krishna"           # Title (Max 20 chars)
NOTIF_MESSAGE = "Ekadashi fast reminder!"   # Subtitle (Max 30 chars)

def run():
    print("\n🚀 [START] Ultra-Fast Direct AppCreator24 Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Login
            print("[1] Opening Login Page...")
            page.goto("https://www.appcreator24.com/", wait_until="domcontentloaded", timeout=40000)
            time.sleep(1)

            print("[2] Submitting Email & Password...")
            page.locator('input[type="text"], input[type="email"], input[name="email"], input[name="user"]').first.fill(EMAIL)
            page.locator('input[type="password"], input[name="password"], input[name="pass"]').first.fill(PASSWORD)
            page.locator('input[type="submit"], button:has-text("Sign in"), input[value*="Sign in"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(3)

            current_url = page.url
            print(f"[3] Current URL after login: {current_url}")

            # Session ID nikalna
            match = re.search(r'idsesion=([a-zA-Z0-9]+)', current_url)
            if not match:
                raise Exception("Login failed or Session ID not found. Check credentials.")
            
            session_id = match.group(1)
            print(f"🔑 [4] Active Session ID Captured: {session_id}")

            # 2. Directly Jump to Send Notifications Page (pag=21)
            notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={session_id}&pag=21&idapp={APP_ID}"
            print(f"[5] Jumping directly to Notifications Page for App ID: {APP_ID}...")
            page.goto(notif_url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)

            # 3. Click New Message
            print("[6] Opening 'New message' form...")
            page.locator('input[value="New message"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 4. Fill Title & Message
            print(f"[7] Typing Title: '{NOTIF_TITLE}' & Subtitle: '{NOTIF_MESSAGE}'...")
            inputs = page.locator('input[type="text"]')
            inputs.nth(0).fill(NOTIF_TITLE)
            inputs.nth(1).fill(NOTIF_MESSAGE)

            # 5. Click Next >>
            print("[8] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            time.sleep(2)

            # 6. Click Send >>
            print("[9] Clicking 'Send >>' to broadcast...")
            page.locator('input[value="Send >>"], input[value*="Send"]').first.click()
            time.sleep(5)

            print("\n" + "="*50)
            print("🎉🎉 SUCCESS: NOTIFICATION SENT SUCCESSFULLY TO USERS! 🎉🎉")
            print("="*50 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ ERROR ENCOUNTERED: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
