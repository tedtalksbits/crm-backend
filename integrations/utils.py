# integrations/utils.py
import requests
import hmac
import hashlib

def trigger_webhook(url, payload, secret=None):
    """
    Helper function to send a webhook payload.
    Includes optional HMAC signature for validation.
    """
    headers = {"Content-Type": "application/json"}
    if secret:
        signature = hmac.new(
            secret.encode('utf-8'),
            msg=str(payload).encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        headers["X-Hub-Signature-256"] = f"sha256={signature}"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log error (or handle it appropriately)
        print(f"Webhook delivery failed: {e}")