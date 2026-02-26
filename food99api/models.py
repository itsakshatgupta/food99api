from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

# -------------------------
# 1️⃣ USER MODEL
# -------------------------
class CustomUser(AbstractUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)    
    location = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
class Otp(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

class BuyerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=150, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    description = models.CharField(max_length=250, blank=True)
    interested_categories = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.user.username


# models.py
class Form(models.Model):
    owner = models.ForeignKey("sellers.Seller", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=50, default="light")
    created_at = models.DateTimeField(auto_now_add=True)

class FormField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=20)  # text, number, image
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

class FormResponse(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)

class FormAnswer(models.Model):
    response = models.ForeignKey(FormResponse, on_delete=models.CASCADE, related_name="answers")
    field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)
