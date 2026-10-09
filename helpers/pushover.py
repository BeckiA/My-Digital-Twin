import os
import requests
from dotenv import load_dotenv

# Enable system certificate validation for Windows/corporate proxies
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

load_dotenv(override=True)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def _check_credentials(user: str | None, token: str | None) -> None:
    if user:
        if user.startswith("u"):
            print("Pushover user found and looks good")
        else:
            print("Pushover user found but doesn't start with u")
    else:
        print("Pushover user not found")

    if token:
        if token.startswith("a"):
            print("Pushover token found and looks good")
        else:
            print("Pushover token found but doesn't start with a")
    else:
        print("Pushover token not found")


# Run initial check at import time
_check_credentials(os.getenv("PUSHOVER_USER"), os.getenv("PUSHOVER_TOKEN"))


def push(message: str) -> bool:
    """Sends a push notification via Pushover API with error handling and fallback."""
    load_dotenv(override=True)
    user = os.getenv("PUSHOVER_USER")
    token = os.getenv("PUSHOVER_TOKEN")

    if not user or not token:
        print(f"[Pushover] Warning: PUSHOVER_USER or PUSHOVER_TOKEN not set in .env")
        return False

    print(f"Push: {message}")
    payload = {"user": user, "token": token, "message": message}

    try:
        response = requests.post(PUSHOVER_URL, data=payload, timeout=10)
        if response.status_code == 200:
            print(f"[Pushover] Notification sent successfully: {response.json()}")
            return True
        else:
            print(f"[Pushover] API returned error status {response.status_code}: {response.text}")
            return False
    except requests.exceptions.SSLError as ssl_err:
        print(f"[Pushover] SSL error ({ssl_err}), retrying with system fallback...")
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(PUSHOVER_URL, data=payload, verify=False, timeout=10)
            if response.status_code == 200:
                print(f"[Pushover] Notification sent successfully (fallback): {response.json()}")
                return True
            else:
                print(f"[Pushover] API returned error status {response.status_code}: {response.text}")
                return False
        except Exception as retry_err:
            print(f"[Pushover] Notification failed on retry: {retry_err}")
            return False
    except Exception as e:
        print(f"[Pushover] Notification error: {e}")
        return False