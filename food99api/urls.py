from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import menu_by_category, CartViewSet
from rest_framework_simplejwt.views import TokenObtainPairView



router = DefaultRouter()
router.register('cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menu/', menu_by_category),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]
