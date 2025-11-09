from rest_framework import viewsets, permissions
from .models import CustomUser, Seller, Product, BuyerProfile, Message, Lead
from .serializers import (
    UserSerializer, SellerSerializer, ProductSerializer,
    BuyerProfileSerializer, MessageSerializer, LeadSerializer
)
from django.contrib.auth import get_user_model
User = get_user_model()


# -------------------------
# USER CRUD
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------
# SELLER CRUD
# -------------------------
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------
# BUYER CRUD
# -------------------------
class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------
# PRODUCT CRUD
# -------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# -------------------------
# MESSAGE CRUD
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------
# LEAD CRUD
# -------------------------
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
