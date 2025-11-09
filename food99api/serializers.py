from rest_framework import serializers
from .models import CustomUser, Seller, Product, BuyerProfile, Message, Lead
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔹 Add custom claims here
        token['user_type'] = user.user_type
        token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'user_type': self.user.user_type,
        }
        return data


# -------------------------
# USER SERIALIZER
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'user_type', 'is_verified']


# -------------------------
# SELLER SERIALIZER
# -------------------------
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = '__all__'


# -------------------------
# BUYER SERIALIZER
# -------------------------
class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BuyerProfile
        fields = '__all__'


# -------------------------
# PRODUCT SERIALIZER
# -------------------------
class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


# -------------------------
# MESSAGE SERIALIZER
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


# -------------------------
# LEAD SERIALIZER
# -------------------------
class LeadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
