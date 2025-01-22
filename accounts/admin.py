from django.contrib import admin
from .models import CustomUser, Company
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.admin import SimpleListFilter

User = get_user_model()

class BotUserFilter(SimpleListFilter):
    """
    Custom filter to toggle the visibility of bot users in the admin.
    """
    title = 'Show Bot Users'
    parameter_name = 'show_bots'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Show Bots'),
            ('no', 'Hide Bots'),
        ]

    def queryset(self, request, queryset):
        # Hide bot users by default
        if self.value() == 'yes':
            return queryset
        elif self.value() == 'no' or not self.value():
            return queryset.exclude(role='bot')
        return queryset
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'company', 'is_active', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'company', BotUserFilter)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_display_links = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    
    def get_queryset(self, request):
        """
        Override the default queryset to hide bot users by default.
        """
        qs = super().get_queryset(request)
        # Exclude bot users unless explicitly included by the filter
        if not request.GET.get('show_bots') or request.GET.get('show_bots') == 'no':
            qs = qs.exclude(role='bot')
        return qs
    
class CompanyAdmin(admin.ModelAdmin):
    # sort by created_at in descending order
    ordering = ('-created_at',)
    list_display = ('name', 'domain', 'owner', 'created_at', 'logo_preview')
    search_fields = ('name', 'domain')
    list_filter = ('owner', 'created_at', 'updated_at', 'subscription_plan')
    
    # show the logo
    readonly_fields = ('logo_preview',)
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="height: 32px; width: 32px; object-fit: cover; border-radius: 100%; aspect-ratio: 1 / 1;" /></a>',
                obj.logo.url, obj.logo.url
            )
        return "No Logo"

    
admin.site.register(Company, CompanyAdmin)
admin.site.register(CustomUser, CustomUserAdmin)