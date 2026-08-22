import sys
import re
import requests

EMAIL = "king123grt@gmail.com"
PASSWORD = "santosh@29"
APP_ID = "4050991"                     # Iskcon Padyatra

NOTIF_TITLE = "Hare Krishna"           # Title
NOTIF_MESSAGE = "Ekadashi fast reminder!"   # Message

def run():
    print("🚀 [START] Direct HTTP Fast Bot...")
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    })

    # 1. Login Request
    print("[1] Sending Login Request to AppCreator24...")
    login_url = "https://www.appcreator24.com/android-creator.php"
    login_data = {
        "email": EMAIL,
        "password": PASSWORD,
        "idioma": "en"
    }

    res = s.post(login_url, data=login_data, allow_redirects=True)
    
    # Session ID nikaalna
    idsesion = None
    match = re.search(r'idsesion=([a-zA-Z0-9]+)', res.text + " " + res.url)
    if match:
        idsesion = match.group(1)
    elif 'idsesion' in s.cookies:
        idsesion = s.cookies['idsesion']

    if not idsesion:
        # Check main page
        res_main = s.get("https://www.appcreator24.com/intra/intra.php?idioma=en&pag=2")
        match = re.search(r'idsesion=([a-zA-Z0-9]+)', res_main.text + " " + res_main.url)
        if match:
            idsesion = match.group(1)

    if not idsesion:
        print("❌ Login Failed! AppCreator24 ne Cloud IP reject kiya ya credentials match nahi hue.")
        sys.exit(1)

    print(f"🔑 [2] Session ID Captured: {idsesion}")

    # 2. Direct Send Notification POST Request
    print(f"[3] Posting Notification to App ID: {APP_ID}...")
    post_notif_url = f"https://www.appcreator24.com/intra/intra.php?idioma=en&idsesion={idsesion}&pag=21&idapp={APP_ID}"
    
    notif_payload = {
        "titulo": NOTIF_TITLE,
        "subtitulo": NOTIF_MESSAGE,
        "tipo_dest": "0",
        "accion": "0",
        "btn_enviar": "Send >>",
        "enviar": "1"
    }

    send_res = s.post(post_notif_url, data=notif_payload)

    if send_res.status_code == 200:
        print("\n" + "="*50)
        print("🎉🎉 100% SUCCESS: NOTIFICATION SENT DIRECTLY! 🎉🎉")
        print("="*50 + "\n")
    else:
        print(f"❌ Failed with status: {send_res.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    run()
