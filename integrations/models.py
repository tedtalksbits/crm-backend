# integrations/models.py
from django.db import models
from accounts.models import Company
class Webhook(models.Model):
    event = models.CharField(max_length=255, help_text="The event that will trigger this webhook. E.g. lead_created, lead_updated, etc.")
    url = models.URLField(help_text="The URL that will receive the webhook payload.")
    description = models.TextField(blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='webhooks', help_text="The company that this webhook belongs to.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Webook for {self.event} at {self.url} (Company: {self.company.name})"
