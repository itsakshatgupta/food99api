from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import menu_by_category, CartViewSet,SignupView,me
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register('cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menu/', menu_by_category),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 👈 add this
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/me/', me, name='me'),
    
    # New payment-related URLs
    path('api/payments/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify_payment'),
]

