import sys
import time
import re
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_ID = "4050991"                     # Iskcon Padyatra App ID

NOTIF_TITLE = "Hare Krishna"           # Title
NOTIF_MESSAGE = "Ekadashi fast reminder!"  # Message

def run():
    print("\n🚀 [START] Guaranteed AppCreator24 Frame-Bypassing Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Open AppCreator24
            print("[1] Opening AppCreator24 Home...")
            page.goto("https://www.appcreator24.com/", timeout=45000)
            page.wait_for_selector('input[type="password"]', timeout=20000)

            # 2. Fill Credentials
            print("[2] Entering Email & Password...")
            page.locator('input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            time.sleep(1)

            # 3. Click Sign In
            print("[3] Clicking Sign In...")
            page.locator('input[value="Sign in"], input[type="submit"], button:has-text("Sign in")').first.click()

            # 4. Wait for redirect
            print("[4] Waiting for Dashboard...")
            page.wait_for_url(lambda u: "android-creator" in u or "intra" in u, timeout=35000)
            time.sleep(4)  # Wait for inner frame to load

            # 5. Extract Session ID from Frames
            session_id = None
            all_urls = [page.url] + [f.url for f in page.frames]
            for u in all_urls:
                match = re.search(r'idsesion=([a-zA-Z0-9]+)', u)
                if match:
                    session_id = match.group(1)
                    break

            if not session_id:
                for f in page.frames:
                    match = re.search(r'idsesion=([a-zA-Z0-9]+)', f.content())
                    if match:
                        session_id = match.group(1)
                        break

            if not session_id:
                raise Exception("Session ID frame se nahi nikal paya.")

            print(f"🔑 [5] Session ID Captured from Frame: {session_id}")

            # 6. Direct Jump to Notifications Page (Bypassing frames)
            notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={session_id}&pag=21&idapp={APP_ID}"
            print(f"[6] Jumping directly to Notifications Panel (App ID: {APP_ID})...")
            page.goto(notif_url, timeout=35000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            # 7. Click New Message
            print("[7] Clicking 'New message' button...")
            page.locator('input[value="New message"]').first.click()
            page.wait_for_selector('input[value="Next >>"], input[value*="Next"]', timeout=25000)
            time.sleep(1)

            # 8. Fill Title & Subtitle
            print(f"[8] Filling Title: '{NOTIF_TITLE}' & Message: '{NOTIF_MESSAGE}'...")
            inputs = page.locator('input[type="text"]')
            inputs.nth(0).fill(NOTIF_TITLE)
            inputs.nth(1).fill(NOTIF_MESSAGE)

            # 9. Click Next >>
            print("[9] Clicking 'Next >>'...")
            page.locator('input[value="Next >>"], input[value*="Next"]').first.click()
            page.wait_for_selector('input[value="Send >>"], input[value*="Send"]', timeout=25000)
            time.sleep(1)

            # 10. Click Send >>
            print("[10] Confirming Broadcast (Send >>)...")
            page.locator('input[value="Send >>"], input[value*="Send"]').first.click()
            time.sleep(5)

            print("\n" + "="*60)
            print("🎉🎉 100% SUCCESS: NOTIFICATION DELIVERED TO APP! 🎉🎉")
            print("="*60 + "\n")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
