from rest_framework import serializers
from .models import CustomUser, BuyerProfile
from sellers.models import Seller
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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'user_type', 'phone')

    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        user = CustomUser.objects.create_user(**validated_data)
        # Auto-create profile based on user_type
        if user_type == 'seller':
            Seller.objects.create(user=user, company_name="")  # will update later

        elif user_type == 'buyer':
            BuyerProfile.objects.create(user=user)

        return user

# -------------------------
# USER SERIALIZER
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'is_verified']


# -------------------------
# BUYER SERIALIZER
# -------------------------
class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BuyerProfile
        fields = '__all__'



     
from .models import Form, FormField, FormResponse, FormAnswer

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'type', 'required', 'order']
        
class FormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'theme', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop("fields")
        form = Form.objects.create(owner=self.context["request"].user, **validated_data)

        for i, f in enumerate(fields_data):
            FormField.objects.create(form=form, order=i, **f)

        return form
