from django.db import models 
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Admin'),
      ('manager', 'Manager'),
      ('sales', 'Sales'),
      ('viewer', 'Viewer'),
      ('customer', 'Customer'),
  )
  
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')