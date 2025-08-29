from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings   # <-- for CustomUser reference
from cloudinary.models import CloudinaryField

# Custom User
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = CloudinaryField('image', folder='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username

# Menu Category 
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Menu Item
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image', folder='menu_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')

    def __str__(self):
        return self.name

# Cart
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- updated
    items = models.ManyToManyField(MenuItem, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

# Cart Item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
