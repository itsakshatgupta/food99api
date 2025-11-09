from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import (
    HomeSectionsView, RegisterView, UserViewSet, BuyerProfileViewSet, SellerViewSet, ProductViewSet, MessageViewSet, LeadViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'buyers', BuyerProfileViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'leads', LeadViewSet)

urlpatterns = [
    path('home-sections/', HomeSectionsView.as_view(), name='home-sections'),
    path('register/', UserViewSet.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]