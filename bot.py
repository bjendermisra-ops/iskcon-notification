import sys
import time
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_NAME = "Iskcon Padyatra"
APP_ID = "4050991"

NOTIF_TITLE = "Hare Krishna"
NOTIF_MESSAGE = "Ekadashi fast reminder!"

def smart_click(page, selectors, desc, timeout=35):
    print(f"👉 Clicking: {desc}...")
    start = time.time()
    while time.time() - start < timeout:
        for frame in page.frames:
            for sel in selectors:
                try:
                    loc = frame.locator(sel).first
                    if loc.count() > 0 and loc.is_visible():
                        loc.click(timeout=3000)
                        time.sleep(3)
                        return True
                except Exception:
                    pass
        time.sleep(1)
    
    # Agar nahi mila toh saare links print karega
    all_links = []
    for frame in page.frames:
        try:
            texts = frame.locator('a').all_inner_texts()
            all_links.extend([t.strip() for t in texts if t.strip()])
        except:
            pass
    print(f"\n⚠️ Page par ye links mile: {all_links}")
    raise Exception(f"Element nahi mila: {desc}")

def smart_fill_form(page, title, message, timeout=35):
    print(f"👉 Filling Title: '{title}' & Subtitle: '{message}'...")
    start = time.time()
    while time.time() - start < timeout:
        for frame in page.frames:
            try:
                inputs = frame.locator('input[type="text"]')
                if inputs.count() >= 2:
                    inputs.nth(0).fill(title)
                    inputs.nth(1).fill(message)
                    time.sleep(1)
                    return True
            except Exception:
                pass
        time.sleep(1)
    raise Exception("Notification input fields nahi mile!")

def run():
    print("\n🚀 [START] Ultra-Resilient AppCreator24 Bot...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. Login Page
            print("[1] Opening AppCreator24...")
            page.goto("https://www.appcreator24.com/", timeout=45000)
            page.wait_for_selector('input[type="password"]', timeout=20000)

            # 2. Enter Credentials
            print("[2] Entering Credentials...")
            page.locator('input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            time.sleep(1)

            # 3. Sign In
            print("[3] Submitting Login...")
            page.locator('input[value="Sign in"], input[type="submit"], button:has-text("Sign in")').first.click()
            
            # Wait until Dashboard / Apps page loads
            print("[4] Waiting for Dashboard page to fully load...")
            time.sleep(8)

            # 4. Click on Iskcon Padyatra App (App Name OR App ID Link)
            app_selectors = [
                f'a[href*="{APP_ID}"]',
                f'a:has-text("{APP_NAME}")',
                f'text="{APP_NAME}"',
                f'tr:has-text("{APP_NAME}") a'
            ]
            smart_click(page, app_selectors, f"App '{APP_NAME}' (ID: {APP_ID})")

            # 5. Click "Send notifications"
            notif_selectors = [
                'a[href*="pag=21"]',
                'a:has-text("Send notifications")',
                'text="Send notifications"'
            ]
            smart_click(page, notif_selectors, "Send notifications menu")

            # 6. Click "New message"
            new_msg_selectors = [
                'input[value="New message"]',
                'a:has-text("New message")',
                'button:has-text("New message")'
            ]
            smart_click(page, new_msg_selectors, "New message button")

            # 7. Fill Notification Form
            smart_fill_form(page, NOTIF_TITLE, NOTIF_MESSAGE)

            # 8. Click Next >>
            smart_click(page, ['input[value="Next >>"]', 'input[value*="Next"]'], "Next >> button")

            # 9. Click Send >>
            smart_click(page, ['input[value="Send >>"]', 'input[value*="Send"]'], "Send >> button")
            time.sleep(6)

            print("\n" + "="*60)
            print("🎉🎉 100% SUCCESS: NOTIFICATION DELIVERED TO USERS! 🎉🎉")
            print("="*60 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ FAILED ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
