from django.contrib import admin 
from .models import Lead, LeadNote, LeadHistory, Attachment, Comment, Activity
# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'created_at', 'status')
    list_filter = ('company', 'created_at', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name')
    list_per_page = 50
    
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ('lead', 'text', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('text', 'created_by')
    list_per_page = 50
    
class LeadHistoryAdmin(admin.ModelAdmin):
    list_display = ('lead', 'status', 'assigned_to', 'updated_by', 'updated_at')
    list_filter = ('status', 'assigned_to', 'updated_by', 'updated_at')
    search_fields = ('status', 'assigned_to', 'updated_by')
    list_per_page = 50
    
class AttachmentAdmin(admin.ModelAdmin):   
    list_display = ('activity', 'file', 'created_at')
    list_filter = ('activity', 'created_at')
    search_fields = ('activity', 'file')
    list_per_page = 50
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('activity', 'text', 'created_by', 'created_at')
    list_filter = ('activity', 'created_by', 'created_at')
    search_fields = ('activity', 'text', 'created_by')
    list_per_page = 50
    
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'type', 'details', 'due_date', 'is_completed', 'completed_at', 'created_at', 'updated_at')
    list_filter = ('lead', 'type', 'due_date', 'is_completed', 'completed_at', 'created_at', 'updated_at')
    search_fields = ('lead', 'type', 'details')
    list_per_page = 50
    
admin.site.register(Lead, LeadAdmin)
admin.site.register(LeadNote, LeadNoteAdmin)
admin.site.register(LeadHistory, LeadHistoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Activity, ActivityAdmin)
