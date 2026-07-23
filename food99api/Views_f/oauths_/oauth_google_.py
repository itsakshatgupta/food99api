import os
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from food99api.models import CustomUser
from food99api.serializers import RegisterSerializer
from food99api.views import generate_username

class GoogleLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
        # Get token sent from Next.js
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            name = idinfo.get("name")
            
            # Check if user already exists
            user = CustomUser.objects.filter(email=email).first()

            # If not, create user
            if not user:
                u = generate_username()
                serializer = RegisterSerializer(data={
                    "username": u,
                    "first_name": name,
                    "email": email,
                    "user_type": "buyer",
                    "auth_provider": "google",
                    # Don't send a password
                })

                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                # Mark as Google account
                user.set_unusable_password()
                user.is_verified = True
                user.save()

            # Generate JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            })

        except ValueError:
            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST
            )
