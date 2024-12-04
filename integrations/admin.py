from django.contrib import admin
from .models import Webhook
# Register your models here.
class WebhookAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('event', 'url', 'created_at')

admin.site.register(Webhook, WebhookAdmin)