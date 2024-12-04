# integrations/utils.py
import requests

def trigger_webhook(event, payload):
    from .models import Webhook
    webhooks = Webhook.objects.filter(event=event)
    for webhook in webhooks:
        requests.post(webhook.url, json=payload)
