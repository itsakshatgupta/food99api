from rest_framework import serializers
from food99api.serializers import UserSerializer
from .models import Seller, Product
from food99api.models import CustomUser

# -------------------------
# SELLER SERIALIZER
# -------------------------
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = '__all__'
        

# -------------------------
# PRODUCT SERIALIZER
# -------------------------
class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']

        # remove any seller coming from frontend
        validated_data.pop('seller', None)
        
        seller = Seller.objects.get(user=request.user)

        product = Product.objects.create(
            seller=seller,
            **validated_data
        )
        return product

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('seller', None)  # hide seller when sending GET response
        return data




