# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Company
from .utils import get_crm_bot_user

@receiver(post_save, sender=Company)
def create_bot_user_for_company(sender, instance, created, **kwargs):
    """
    Signal to create a bot user when a new company is created.
    """
    get_crm_bot_user(instance)
