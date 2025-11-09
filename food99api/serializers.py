from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Seller, Product, BuyerProfile, Message, Lead


# ------------------- USER REGISTER -------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        # Auto-create BuyerProfile when a user registers
        BuyerProfile.objects.create(user=user)
        return user


# ------------------- BUYER -------------------
class BuyerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'company_name', 'phone', 'address', 'city', 'state', 'country']
        
# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# --- Seller Serializer ---
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Seller
        fields = '__all__'


# --- Product Serializer ---
class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


# --- Buyer Serializer ---
class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = BuyerProfile
        fields = '__all__'


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


# --- Lead Serializer ---
class LeadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
