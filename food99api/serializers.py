from rest_framework import serializers
from .models import MenuItem, Cart, CartItem, MenuItemVariant
from .models import Category, Order
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number', 'profile_image']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            profile_image=validated_data.get('profile_image') 
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'profile_image']

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url  # full Cloudinary URL
        return None

# Nested serializer for the variant with its specific price
class MenuItemVariantSerializer(serializers.ModelSerializer):
    variant_name = serializers.CharField(source='variant.name')  # show variant name

    class Meta:
        model = MenuItemVariant
        fields = ['variant_name', 'price']


class MenuItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    variant = MenuItemVariantSerializer(source='menuitemvariant_set', many=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'image', 'price', 'variant']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)  # nested items

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()  # nested serializer

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'menu_item']  # no need for 'cart'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = '__all__'   # includes id, user, created_at, and items

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"