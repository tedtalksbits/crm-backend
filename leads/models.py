from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('unassigned', 'Unassigned'),
        ('contacted', 'Contacted'),
        ('converted', 'Converted'),
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
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"