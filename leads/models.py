from django.db import models
from accounts.models import CustomUser, Company
# Create your models here.
class Lead(models.Model):
    STATUS_CHOICES = (
    ('new', 'New'),
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('qualified', 'Qualified'),
    ('proposal_sent', 'Proposal Sent'),
    ('negotiation', 'Negotiation'),
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('closed', 'Closed'),
)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leads', help_text="The company that owns this lead.")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Activity(models.Model):
    ACTIVITY_TYPE_CHOICES = (
        ('email', 'Email'),
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('sms', 'SMS'),
        ('other', 'Other'),
    )
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, default='email')
    details = models.TextField()
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.type} for {self.lead.first_name} {self.lead.last_name}"
    
    class Meta:
        verbose_name_plural = "Activities"

class Attachment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.activity.lead.first_name} {self.activity.lead.last_name}"


class Comment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.created_by.username} for {self.activity.lead.first_name} {self.activity.lead.last_name}"
    

class LeadHistory(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20, choices=Lead.STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads_histories')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_leads_histories')
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for {self.lead.first_name} {self.lead.last_name}"
    
    class Meta:
        verbose_name_plural = "Lead Histories"
        ordering = ['-updated_at']
        
class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Note by {self.created_by.username} for {self.lead.first_name} {self.lead.last_name}"