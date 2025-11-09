from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import (
    HomeSectionsView, RegisterView, BuyerProfileViewSet, SellerViewSet, ProductViewSet, MessageViewSet, LeadViewSet
)

router = DefaultRouter()
router.register(r'buyers', BuyerProfileViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'leads', LeadViewSet)

urlpatterns = [
    path('api/home-sections/', HomeSectionsView.as_view(), name='home-sections'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]