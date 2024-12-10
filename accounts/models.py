from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Admin'),
      ('manager', 'Manager'),
      ('sales', 'Sales'),
      ('viewer', 'Viewer'),
      ('customer', 'Customer'),
      ('bot', 'Bot'),
  )
  
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
  company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
  phone = models.CharField(max_length=20, null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
  is_active = models.BooleanField(default=True)  # Whether the user account is active
  last_login_ip = models.GenericIPAddressField(null=True, blank=True)  # Last login IP address
  failed_login_attempts = models.IntegerField(default=0)  # Number of failed login attempts
  last_failed_login = models.DateTimeField(null=True, blank=True)  # Timestamp of the last failed login attempt
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  
# accounts/models.py
from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=255)
  logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
  domain = models.CharField(max_length=255, unique=True)  # e.g., company-specific domain
  address = models.TextField(null=True, blank=True)
  phone = models.CharField(max_length=20, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  website = models.URLField(null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='companies')
  subscription_plan = models.CharField(max_length=50, null=True, blank=True) # e.g., free, basic, premium
  subscription_expiry = models.DateField(null=True, blank=True) # date when the subscription expires
  max_users = models.IntegerField(default=10) # maximum number of users allowed
  max_storage_size = models.IntegerField(default=1024)  # in MB
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    verbose_name_plural = "Companies"

  def __str__(self):
    return self.name


class Invitation(models.Model):
  email = models.EmailField()
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  invited_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_invitations")
  token = models.CharField(max_length=255, unique=True)  # Generated unique token
  is_accepted = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Invitation to {self.email} for {self.company.name}"
