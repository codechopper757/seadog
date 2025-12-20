import requests
from utils.config import ConfigManager


def send_gotify_notification(title: str, message: str):
    config = ConfigManager()

    if not config.get("gotify_enabled", False):
        return

    url = config.get("gotify_url", "").rstrip("/")
    token = config.get("gotify_token", "")

    if not url or not token:
        return

    endpoint = f"{url}/message?token={token}"

    payload = {
        "title": title,
        "message": message,
        "priority": 5
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
    except Exception:
        # Intentionally silent — no secrets, no spam
        pass
