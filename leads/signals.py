# leads/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Lead, LeadNote
from integrations.utils import trigger_webhook
from integrations.models import Webhook
from accounts.utils import get_crm_bot_user

@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    """
    Trigger webhooks for lead creation or updates, scoped to the company's webhooks.
    """
    event = 'lead_created' if created else 'lead_updated'
    payload = {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "status": instance.status,
        "company": instance.company.name
    }

    # Retrieve all webhooks for the company and the specific event
    webhooks = Webhook.objects.filter(company=instance.company, event=event)
    for webhook in webhooks:
        trigger_webhook(webhook.url, payload, secret=webhook.secret)

# use bot to create a lead note
@receiver(post_save, sender=Lead)
def create_bot_note_for_lead(sender, instance, created, **kwargs):
    if created:
        bot_user = get_crm_bot_user(instance.company)
        note_text = f"A new lead '{instance.first_name} {instance.last_name}' has been created."
        LeadNote.objects.create(
            lead=instance,
            text=note_text,
            created_by=bot_user
        )
        
# use bot to track lead status changes
@receiver(pre_save, sender=Lead)
def track_lead_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Lead.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            instance._old_status = old_instance.status  # Track the old status
            
            
@receiver(post_save, sender=Lead)
def create_bot_note_for_status_change(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_old_status'):
        bot_user = get_crm_bot_user(instance.company)
        old_status = instance._old_status
        new_status = instance.status
        note_text = f"Lead '{instance.first_name} {instance.last_name}' status changed from '{old_status}' to '{new_status}'."
        LeadNote.objects.create(
            lead=instance,
            text=note_text,
            created_by=bot_user
        )