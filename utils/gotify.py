import requests
from utils.config import ConfigManager

def send_gotify_notification(title: str, message: str, priority: int = 5):
    """
    Sends a Gotify notification using the token and URL in config.json.
    """
    config = ConfigManager()
    gotify_url = config.get("gotify_url", "").rstrip("/")
    gotify_token = config.get("gotify_token", "")

    if not gotify_url or not gotify_token:
        print("Gotify URL or token not set in config.")
        return

    payload = {
        "title": title,
        "message": message,
        "priority": priority
    }

    headers = {
        "X-Gotify-Key": gotify_token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{gotify_url}/message", json=payload, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Gotify notification: {e}")
