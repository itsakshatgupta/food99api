from django.contrib import admin

# Register your models here.
from .models import MenuItem, Cart, CartItem, Category,MenuVariant, MenuItemVariant

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuVariant)
admin.site.register(MenuItemVariant)
admin.site.register(Cart)
admin.site.register(CartItem)
