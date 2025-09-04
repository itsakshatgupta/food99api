from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import menu_by_category, CartViewSet,SignupView,me
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import CreateOrderView, VerifyPaymentView, CartItemViewSet, test

router = DefaultRouter()
router.register("cart/items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path('', include(router.urls)),
    path('menu/', menu_by_category),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 👈 add this
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/me/', me, name='me'),
    path('cart', CartViewSet, name='me'),
    path('test', test, name='test'),
    
    *router.urls,
    
    # New payment-related URLs
    path('api/payments/create-order/', CreateOrderView.as_view(), name='initiate_payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify_payment'),
]

