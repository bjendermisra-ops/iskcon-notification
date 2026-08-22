import sys
import time
from playwright.sync_api import sync_playwright

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_NAME = "Iskcon Padyatra"

NOTIF_TITLE = "Hare Krishna"
NOTIF_MESSAGE = "Ekadashi fast reminder!"

def smart_click(page, selector, desc, timeout=30):
    """Ye function har frame me jakar button/link dhoond kar click karta hai"""
    print(f"👉 Clicking: {desc}...")
    start = time.time()
    while time.time() - start < timeout:
        for frame in page.frames:
            try:
                loc = frame.locator(selector).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click()
                    time.sleep(2)
                    return True
            except Exception:
                pass
        time.sleep(1)
    raise Exception(f"Element nahi mila: {desc} ({selector})")

def smart_fill_form(page, title, message, timeout=30):
    """Notification form bharne ke liye"""
    print("👉 Filling Title and Subtitle...")
    start = time.time()
    while time.time() - start < timeout:
        for frame in page.frames:
            try:
                inputs = frame.locator('input[type="text"]')
                if inputs.count() >= 2 and inputs.first.is_visible():
                    inputs.nth(0).fill(title)
                    inputs.nth(1).fill(message)
                    time.sleep(1)
                    return True
            except Exception:
                pass
        time.sleep(1)
    raise Exception("Notification input fields nahi mile!")

def run():
    print("\n🚀 [START] Smart Frame Clicker Bot Running...")
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
            time.sleep(2)

            print("[2] Entering Email and Password...")
            page.locator('input[type="text"], input[type="email"]').first.fill(EMAIL)
            page.locator('input[type="password"]').first.fill(PASSWORD)
            time.sleep(1)

            # 2. Sign In
            print("[3] Submitting Login...")
            page.locator('input[value="Sign in"], input[type="submit"], button:has-text("Sign in")').first.click()
            time.sleep(6)  # Frames load hone ka wait

            # 3. Click on App Name (Iskcon Padyatra)
            smart_click(page, f'a:has-text("{APP_NAME}"), text="{APP_NAME}"', f"App ({APP_NAME})")

            # 4. Click Send notifications
            smart_click(page, 'text="Send notifications", a:has-text("Send notifications")', "Send notifications menu")

            # 5. Click New message
            smart_click(page, 'input[value="New message"]', "New message button")

            # 6. Fill Title & Subtitle
            smart_fill_form(page, NOTIF_TITLE, NOTIF_MESSAGE)

            # 7. Click Next >>
            smart_click(page, 'input[value="Next >>"], input[value*="Next"]', "Next >> button")

            # 8. Click Send >>
            smart_click(page, 'input[value="Send >>"], input[value*="Send"]', "Send >> button")
            time.sleep(5)

            print("\n" + "="*60)
            print("🎉🎉 100% SUCCESS: NOTIFICATION SENT SUCCESSFULLY! 🎉🎉")
            print("="*60 + "\n")

        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print(f"\n❌ FAILED ERROR: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
