import requests
from utils.config import ConfigManager


def send_gotify_notification(title: str, message: str):
    """
    Used by downloads.
    Silent, config-driven, no UI errors.
    """
    config = ConfigManager()

    url = config.get("gotify_url", "").rstrip("/")
    token = config.get("gotify_token", "")

    if not url or not token:
        return

    endpoint = f"{url}/message?token={token}"

    payload = {
        "title": title,
        "message": message,
        "priority": 5,
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
    except Exception:
        # Silent by design for background notifications
        pass


def test_gotify_notification(title: str, message: str, url: str, token: str):
    """
    Used ONLY by the Settings tab test button.
    Loud, explicit, raises errors.
    """
    if not url or not token:
        raise ValueError("Gotify URL or token missing")

    endpoint = f"{url.rstrip('/')}/message?token={token}"

    payload = {
        "title": title,
        "message": message,
        "priority": 5,
    }

    response = requests.post(endpoint, json=payload, timeout=10)
    response.raise_for_status()
