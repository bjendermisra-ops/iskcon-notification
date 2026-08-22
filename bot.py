import os
import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ==================== आपकी डिटेल्स ====================
EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"

APP_NAME = "Iskcon Padyatra"          # App Name (Exact)
NOTIF_TITLE = "Hare Krishna"          # Title (Max 20 chars)
NOTIF_MESSAGE = "Ekadashi fast reminder!"  # Subtitle (Max 30 chars)
# ======================================================

def print_error_box(reason, fix):
    print("\n" + "="*60)
    print("❌ ERROR OCCURRED! / समस्या आ गई है:")
    print(f"📌 REASON (कारण): {reason}")
    print(f"🛠️  HOW TO FIX (समाधान): {fix}")
    print("="*60 + "\n")

def run():
    print("\n🚀 [SYSTEM START] Initializing Super-Powered AppCreator24 Bot...")
    stage = "INITIALIZATION"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        try:
            # ----------------------------------------------------
            # STAGE 1: LOGIN
            # ----------------------------------------------------
            stage = "LOGIN_PAGE"
            print("\n[Stage 1] AppCreator24 Login पेज खोला जा रहा है...")
            page.goto("https://www.appcreator24.com/login.php", timeout=45000)
            
            print("[Stage 1] Email और Password भरे जा रहे हैं...")
            page.fill('input[type="text"], input[type="email"], input[name="email"]', EMAIL)
            page.fill('input[type="password"], input[name="password"]', PASSWORD)
            page.click('input[type="submit"], button:has-text("Sign in")')
            page.wait_for_load_state("networkidle", timeout=30000)

            # Check if login succeeded
            if "login" in page.url.lower():
                body_text = page.inner_text("body")
                page.screenshot(path="error_screenshot.png")
                print_error_box(
                    reason="Login Failed! (लॉगिन नहीं हुआ - गलत ईमेल या पासवर्ड हो सकता है)",
                    fix="कृपया चेक करें कि पासवर्ड 'santosh@29' सही है या AppCreator24 पर कोई Captcha तो नहीं आ रहा।"
                )
                sys.exit(1)
            
            print("✅ [Stage 1 Success] Login सफल हो गया!")

            # ----------------------------------------------------
            # STAGE 2: FIND & SELECT APP
            # ----------------------------------------------------
            stage = "SELECT_APP"
            print(f"\n[Stage 2] '{APP_NAME}' ऐप ढूंढा जा रहा है...")
            
            # App link check
            app_element = page.locator(f'text="{APP_NAME}"')
            if app_element.count() == 0:
                page.screenshot(path="error_screenshot.png")
                # Available apps list nikaalna
                available_apps = page.locator('table a').all_inner_texts()
                apps_found = ", ".join([a.strip() for a in available_apps if a.strip()])
                print_error_box(
                    reason=f"'{APP_NAME}' नाम का ऐप आपके अकाउंट में नहीं मिला!",
                    fix=f"कोड में APP_NAME को सही करें। आपके अकाउंट में ये ऐप्स मिले: [{apps_found}]"
                )
                sys.exit(1)

            app_element.first.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            print(f"✅ [Stage 2 Success] '{APP_NAME}' ऐप ओपन हो गया!")

            # ----------------------------------------------------
            # STAGE 3: OPEN NOTIFICATIONS
            # ----------------------------------------------------
            stage = "OPEN_NOTIFICATIONS"
            print("\n[Stage 3] 'Send notifications' मेन्यू पर क्लिक किया जा रहा है...")
            
            notif_link = page.locator('text="Send notifications"')
            if notif_link.count() == 0:
                page.screenshot(path="error_screenshot.png")
                print_error_box(
                    reason="'Send notifications' मेन्यू नहीं मिला।",
                    fix="शायद ऐप का साइडबार लोड नहीं हुआ। दोबारा चलाकर देखें।"
                )
                sys.exit(1)

            notif_link.first.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ [Stage 3 Success] Notifications सेक्शन खुल गया!")

            # ----------------------------------------------------
            # STAGE 4: NEW MESSAGE FORM
            # ----------------------------------------------------
            stage = "NEW_MESSAGE_FORM"
            print("\n[Stage 4] 'New message' फॉर्म खोला जा रहा है...")
            page.click('input[value="New message"]')
            page.wait_for_load_state("networkidle", timeout=30000)

            print(f"[Stage 4] Title: '{NOTIF_TITLE}' और Subtitle: '{NOTIF_MESSAGE}' डाला जा रहा है...")
            inputs = page.locator('input[type="text"]')
            if inputs.count() < 2:
                page.screenshot(path="error_screenshot.png")
                print_error_box(
                    reason="नोटिफिकेशन फॉर्म के इनपुट बॉक्स नहीं मिले।",
                    fix="AppCreator24 के फॉर्म लेआउट में बदलाव हुआ हो सकता है।"
                )
                sys.exit(1)

            inputs.nth(0).fill(NOTIF_TITLE)
            inputs.nth(1).fill(NOTIF_MESSAGE)

            # Click Next
            page.click('input[value="Next >>"]')
            page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ [Stage 4 Success] फॉर्म भर गया और Next पेज पर आ गया!")

            # ----------------------------------------------------
            # STAGE 5: CONFIRM AND SEND
            # ----------------------------------------------------
            stage = "CONFIRM_SEND"
            print("\n[Stage 5] 'Send >>' बटन दबाकर नोटिफिकेशन भेजा जा रहा है...")
            
            send_btn = page.locator('input[value="Send >>"]')
            if send_btn.count() == 0:
                page.screenshot(path="error_screenshot.png")
                print_error_box(
                    reason="कन्फर्मेशन पेज पर 'Send >>' बटन नहीं दिखा।",
                    fix="चेक करें कि Title या Subtitle में कोई अमान्य कैरेक्टर तो नहीं है।"
                )
                sys.exit(1)

            send_btn.click()
            time.sleep(6)

            print("\n" + "*"*60)
            print("🎉🎉 100% SUCCESSFUL! NOTIFICATION SENT LIVE TO USERS! 🎉🎉")
            print(f"📱 App: {APP_NAME}")
            print(f"📝 Title: {NOTIF_TITLE}")
            print(f"💬 Message: {NOTIF_MESSAGE}")
            print("*"*60 + "\n")

        except PlaywrightTimeoutError as e:
            page.screenshot(path="error_screenshot.png")
            print_error_box(
                reason=f"Stage [{stage}] पर पेज लोड होने में ज्यादा समय लग गया (Timeout Error)!",
                fix="AppCreator24 का सर्वर धीमा चल रहा है। 2-3 मिनट बाद दोबारा चलाएं।"
            )
            sys.exit(1)
        except Exception as e:
            page.screenshot(path="error_screenshot.png")
            print_error_box(
                reason=f"अनपेक्षित एरर (Stage: {stage}) -> {str(e)}",
                fix="स्क्रीनशॉट Artifacts में सेव हो गया है, उसे चेक करके स्थिति देखें।"
            )
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
