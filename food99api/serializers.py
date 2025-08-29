from rest_framework import serializers
from .models import MenuItem, Cart, CartItem
from .models import Category
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_image']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image']

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)  # nested items

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
