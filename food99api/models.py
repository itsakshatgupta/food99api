from django.db import models
from django.db.models import Sum, F
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

# Menu Variant
class MenuVariant(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    extra = models.TextField()

    def __str__(self):
        return self.name

# Menu Item
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    tags = models.JSONField(default=list)
    image = CloudinaryField('image', folder='menu_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    variant = models.ManyToManyField(MenuVariant, blank=True)  # <-- updated 

    def __str__(self):
        return self.name
    
# Through model to store price per variant per menu item
class MenuItemVariant(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    variant = models.ForeignKey(MenuVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price specific to this item+variant

    class Meta:
        unique_together = ('menu_item', 'variant')  # one variant per item

    def __str__(self):
        return f"{self.menu_item.name} - {self.variant.name} : {self.price}"
    
# Cart
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- updated
    items = models.ManyToManyField(MenuItem, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total(self):
        return self.cartitem_set.aggregate(
        total=Sum(F("menu_item__price") * F("quantity"))
        )["total"] or 0
    
    def __str__(self):
        return self.user.username

# Cart Item
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("COMPLETED", "Completed"), ("FAILED", "Failed")],
        default="PENDING",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.payment_status}"
