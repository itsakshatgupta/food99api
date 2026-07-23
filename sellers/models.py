from django.db import models
from django.conf import settings

class Seller(models.Model):
    BUSINESS_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('agency', 'Agency'),
        ('retailer', 'Retailer'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
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

class Category(models.Model):
   name = models.CharField(max_length=150, unique=True)
   slug = models.SlugField(max_length=200, unique=True)
   
   # parent=null → main category
   parent = models.ForeignKey(
       'self',
       on_delete=models.CASCADE,
       related_name='children',
       null=True,
       blank=True
   )
   
   icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)
   image = models.ImageField(upload_to='categories/images/', blank=True, null=True)
   
   is_active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)
   class Meta:
       verbose_name_plural = "Categories"
   def __str__(self):
       return self.name
   @property
   def is_main_category(self):
       return self.parent is None


 
class Product(models.Model):
   seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
   name = models.CharField(max_length=150)
   description = models.TextField(blank=True)
   price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   moq = models.CharField(max_length=50, blank=True, null=True)  # Minimum Order Quantity
   model_no = models.CharField(max_length=50, blank=True, null=True)  # Minimum Order Quantity
   warranty_detail = models.CharField(max_length=50, blank=True, null=True)  # Minimum Order Quantity
   image = models.ImageField(upload_to='products/images/', blank=True, null=True)
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
   tags = models.JSONField(default=list, blank=True)
   delivery_available = models.CharField(max_length=50, blank=True, null=True)
   views = models.CharField(max_length=50, default=0)
   enquires = models.CharField(max_length=50, default=0)
   status = models.CharField(max_length=50, default='Active')
   installation_available = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return f"{self.name} ({self.seller.company_name})"