from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
class Seller(models.Model):
    BUSINESS_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('agency', 'Agency'),
        ('retailer', 'Retailer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=150)
    business_type = models.CharField(max_length=30, choices=BUSINESS_TYPES)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    logo = models.ImageField(upload_to='sellers/logos/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    moq = models.CharField(max_length=50, blank=True, null=True)  # Minimum Order Quantity
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    stock_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.seller.company_name})"
class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=150, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    interested_categories = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    message_type = models.CharField(
        max_length=20,
        choices=[('text', 'Text'), ('image', 'Image'), ('enquiry', 'Enquiry')],
        default='text'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"
class Lead(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    enquiry_text = models.TextField(blank=True)
    source = models.CharField(max_length=50, default='website')  # or 'whatsapp', 'call'
    status = models.CharField(
        max_length=20,
        choices=[('new', 'New'), ('contacted', 'Contacted'), ('closed', 'Closed')],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)
