from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import (
    HomeSectionsView, LogoutView,  RegisterView, UserViewSet, BuyerProfileViewSet, CustomTokenObtainPairView, FormViewSet, VerifyOtpView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'register', RegisterView,basename='register')
router.register(r'buyers', BuyerProfileViewSet)
router.register('forms', FormViewSet, basename='forms')

urlpatterns = [
    path('home-sections/', HomeSectionsView.as_view(), name='home-sections'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view()),
    path('verify-otp/<uuid:otp_uuid>/<str:email>/', VerifyOtpView.as_view()),
    path('', include(router.urls)),
]