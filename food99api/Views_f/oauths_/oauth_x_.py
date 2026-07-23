import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import settings, status
import os

class XLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        code = request.data.get("code")
        code_verifier = request.data.get("code_verifier")

        if not code:
            return Response(
                {"error": "Authorization code required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Exchange code for access token
            token_response = requests.post(
                "https://api.x.com/2/oauth2/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "code": code,
                    "grant_type": "authorization_code",
                    "client_id": settings.X_CLIENT_ID,
                    "redirect_uri": settings.X_REDIRECT_URI,
                    "code_verifier": code_verifier,
                }
            )

            token_data = token_response.json()

            if "access_token" not in token_data:
                return Response(
                    {
                        "error": "Failed to get X access token",
                        "details": token_data
                    },
                    status=400
                )


            access_token = token_data["access_token"]


            # Get X user profile
            user_response = requests.get(
                "https://api.x.com/2/users/me",
                headers={
                    "Authorization": f"Bearer {access_token}"
                },
                params={
                    "user.fields": "profile_image_url,name,username"
                }
            )


            x_user = user_response.json()


            return Response({
                "x_user": x_user,
                "token": token_data
            })


        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500
            )