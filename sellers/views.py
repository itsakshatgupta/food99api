from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions
from .models import Seller, Product
from .serializers import (
   SellerSerializer, ProductSerializer
)


# -------------------------
# SELLER CRUD
# -------------------------
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.user_type=="seller":
            raise PermissionDenied("Already a seller")
        
        with transaction.atomic():
            serializer.save(user=user)
            user.user_type="seller"
            user.save(update_fields=["user_type"])
            


# -------------------------
# PRODUCT CRUD
# -------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        # This injects the currently logged-in user (request.user) 
        # as the 'seller' before saving the product. 
        serializer.save(seller=self.request.user)
    def get_queryset(self):
        print('s___:', self.request.user)
        seller = Seller.objects.get(user=self.request.user)
        print('s:', seller.joined_on)
        return Product.objects.filter(seller=seller).order_by('-created_at')

