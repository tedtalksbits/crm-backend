# leads/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from integrations.utils import trigger_webhook

@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    event = 'lead_created' if created else 'lead_updated'
    payload = {'id': instance.id, 'name': instance.name, 'status': instance.status}
    trigger_webhook(event, payload)
