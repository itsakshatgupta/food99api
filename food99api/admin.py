from django.contrib import admin

# Register your models here.
from .models import MenuItem, Cart, CartItem, Category

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(CartItem)
