from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, BuyerProfile
from .serializers import (
    UserSerializer, BuyerProfileSerializer
)
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.decorators import action
from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework.views import APIView
from sellers.models import Seller
from lead.permissions import IsSeller
from food99api.models import BuyerProfile
from rest_framework.decorators import action
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random

class RegisterView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save user (inactive until OTP verified - optional)
        user = serializer.save(is_active=False)
        # Generate OTP
        otp = random.randint(100000, 999999)
        # For testing only (later store in DB)
        # Send Email using SendGrid
        message = Mail(
            from_email="otp@tradeb2b.online",  # must be verified in SendGrid
            to_emails=user.email,
            subject="Your OTP Code",
            html_content=f"<strong>Your OTP is {otp}</strong>"
        )
        try:
            sg = SendGridAPIClient("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")
            sg.send(message)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "message": "User registered. OTP sent to email.",
                "otp": "123"  # ⚠️ remove in production
            },
            status=status.HTTP_201_CREATED
        )
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            rt = request.data.get("refresh")
            print(1, rt)
            token = RefreshToken(rt)
            token.blacklist()
            return Response("success")
        except Exception as e:
            print('ex:', request.data)
            return Response({"error":f"Invaild or expired token"}, status=400)
    
# -------------------------
# USER CRUD
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print(user.id)
        return User.objects.filter(id=user.id, username=user.username)
    
    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated, IsSeller])
    def search_(self, request):
        user_queryset = BuyerProfile.objects.filter(user__user_type="buyer")
        serializer = BuyerProfileSerializer(
            user_queryset,
            many=True,
            context={"request":request}            
        )
        return Response(serializer.data)
              


# -------------------------
# BUYER CRUD
# -------------------------
class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]



from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class HomeSectionsView(APIView):
    def get(self, request, *args, **kwargs ):
        sections = [ 
            { "id": 1, "type": "offers", "title": "🔥 Offers for You", "gridCol": 2, "color_theme_name":'fresh vibe', "overflowX": False, "items": [ { "title": "50% OFF on First Order", "code": "WELCOME50", "image": "/test_img/nmk5.jpg", "bg": "bg-gradient-to-r from-blue-500 to-indigo-500" }, { "title": "Free Delivery Above ₹199", "code": "FREESHIP", "image": "/test_img/nmk2.png", "bg": "bg-gradient-to-r from-green-400 to-emerald-500" }, { "title": "10% Cashback via UPI", "code": "UPI10", "image": "/test_img/nmk3.jpeg", "bg": "bg-gradient-to-r from-rose-400 to-pink-500" }, { "title": "Flat ₹75 OFF for Students", "code": "STUDENT75", "image": "/test_img/nmk4.jpg", "bg": "bg-gradient-to-r from-amber-400 to-orange-500" }, ], }, { "id": 2, "type": "category_grid", "title": "🍱 Popular Categories", "color_theme_name":'focus vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Clothes", "items": [ { "name": "Noodles", "image": "/test_img/nmk3.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk4.jpg" }, { "name": "Juices", "image": "/test_img/nmk7.jpeg" }, ], }, { "sub_cat": "Foods", "items": [ { "name": "Noodles", "image": "/test_img/nmk3.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk4.jpg" }, { "name": "Juices", "image": "/test_img/nmk7.jpeg" }, ], }, { "sub_cat": "Households", "items": [ { "name": "Noodles", "image": "/test_img/nmk3.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk4.jpg" }, { "name": "Juices", "image": "/test_img/nmk7.jpeg" }, ], }, ], }, { "id": 3, "type": "search_suggestion", "title": "Are you looking these?", "gridCol": 2, "overflowX": False, "items": [ { "name": "Hakka Noodles", "image": "/test_img/nmk5.jpg", "api": "/api/menu/trending" }, { "name": "Pizza Sauce", "image": "/test_img/nmk4.jpg", "api": "/api/menu/trending" }, { "name": "Healthy Juices", "image": "/test_img/nmk7.jpeg", "api": "/api/menu/trending" }, ], }, { "id": 5, "type": "product_grid", "title": "🍱 Featured Products", "gridCol": False, "overflowX": True, "items": [ { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.jpeg" }, { "name": "Juices", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, { "name": "Pizza", "image": "/test_img/bs2.webp" }, { "name": "Juices", "image": "/test_img/bs1.webp" }, ], }, { "id": 1, "type": "category_grid", "title": "🔥 Up to 70% Off — Deal Festival", "color_theme_name":'discover vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Gourmet Snacks", "items": [ { "name": "Sesame Crackers", "image": "/test_img/nmk13.jpg" }, { "name": "Rice Chips", "image": "/test_img/nmk15.webp" }, { "name": "Oat Bites", "image": "/test_img/nmk14.jpeg" }, { "name": "Coconut Crisps", "image": "/test_img/nmk12.webp" }, { "name": "Cumin Sticks", "image": "/test_img/nmk14.png" }, ] }, { "sub_cat": "Hydration Essentials", "items": [ { "name": "Vitamin Water", "image": "/test_img/nmk14.png" }, { "name": "Energy Sipper", "image": "/test_img/nmk12.webp" }, { "name": "Aloe Booster", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Pizzeria Favourites", "items": [ { "name": "Thin Crust Slice", "image": "/test_img/nmk14.jpeg" }, { "name": "Cheese Burst", "image": "/test_img/nmk14.png" }, { "name": "NYC Lava Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Mushroom Special", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Gourmet Snacks", "items": [ { "name": "Sesame Crackers", "image": "/test_img/nmk13.jpg" }, { "name": "Rice Chips", "image": "/test_img/nmk15.webp" }, { "name": "Oat Bites", "image": "/test_img/nmk14.jpeg" }, { "name": "Coconut Crisps", "image": "/test_img/nmk12.webp" }, { "name": "Cumin Sticks", "image": "/test_img/nmk14.png" }, ] }, { "sub_cat": "Hydration Essentials", "items": [ { "name": "Vitamin Water", "image": "/test_img/nmk14.png" }, { "name": "Energy Sipper", "image": "/test_img/nmk12.webp" }, { "name": "Aloe Booster", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Pizzeria Favourites", "items": [ { "name": "Thin Crust Slice", "image": "/test_img/nmk14.jpeg" }, { "name": "Cheese Burst", "image": "/test_img/nmk14.png" }, { "name": "NYC Lava Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Mushroom Special", "image": "/test_img/nmk15.webp" }, ] }, ] }, { "id": 2, "type": "category_grid", "title": "🍱 Grab More — Pay Less", "color_theme_name":'fresh vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Asian Bites", "items": [ { "name": "Ramen Bowl", "image": "/test_img/nmk12.webp" }, { "name": "Cheese Pot Rice", "image": "/test_img/nmk15.webp" }, { "name": "Bok Spice Plate", "image": "/test_img/nmk14.png" }, ] }, { "sub_cat": "Energy Boosters", "items": [ { "name": "Guava Boost", "image": "/test_img/nmk13.jpg" }, { "name": "Lychee Rush", "image": "/test_img/nmk14.jpeg" }, { "name": "Mango Power", "image": "/test_img/nmk12.webp" }, { "name": "Berry Aminos", "image": "/test_img/nmk14.png" }, ] }, { "sub_cat": "Baked Specials", "items": [ { "name": "Stuffed Pizza", "image": "/test_img/nmk14.png" }, { "name": "Napoli Slice", "image": "/test_img/nmk13.jpg" }, { "name": "NYC Square", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Instant Heat Meals", "items": [ { "name": "Butter Corn Bowl", "image": "/test_img/nmk13.jpg" }, { "name": "Hot Noodles", "image": "/test_img/nmk14.jpeg" }, { "name": "Spice Mix Pot", "image": "/test_img/nmk12.webp" }, ] }, ] }, { "id": 5, "type": "product_grid", "title": "🍱 Featured Products", "gridCol": False, "overflowX": True, "items": [ { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.jpeg" }, { "name": "Juices", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, { "name": "Pizza", "image": "/test_img/bs2.webp" }, { "name": "Juices", "image": "/test_img/bs1.webp" }, ], }, { "id": 3, "type": "category_grid", "title": "🥡 Deal Fiesta — Max Saver Combo", "color_theme_name":'woman fav', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Italian Crust House", "items": [ { "name": "Roman Crust", "image": "/test_img/nmk14.jpeg" }, { "name": "Cheese Overload", "image": "/test_img/nmk13.jpg" }, { "name": "Firewood Slice", "image": "/test_img/nmk12.webp" }, { "name": "Garlic Toppings", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Refreshing Shots", "items": [ { "name": "Mint Lime", "image": "/test_img/nmk14.png" }, { "name": "Kiwi Boost", "image": "/test_img/nmk15.webp" }, { "name": "Lemon Chill", "image": "/test_img/nmk12.webp" }, { "name": "Berry Punch", "image": "/test_img/nmk14.jpeg" }, ] }, { "sub_cat": "Asian Pot Flare", "items": [ { "name": "Soba Noodles", "image": "/test_img/nmk14.png" }, { "name": "Korean Spicy", "image": "/test_img/nmk14.jpeg" }, { "name": "Thai Crack Mix", "image": "/test_img/nmk13.jpg" }, ] }, ] }, { "id": 4, "type": "category_grid", "title": "🍕 Crazy Combo Drop — Deal Bomb", "color_theme_name":'discover vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Fusion Slices", "items": [ { "name": "Volcano Slice", "image": "/test_img/nmk14.jpeg" }, { "name": "Hot Pepperoni", "image": "/test_img/nmk15.webp" }, { "name": "Smoked Special", "image": "/test_img/nmk13.jpg" }, { "name": "BBQ Deluxe", "image": "/test_img/nmk12.webp" }, ] }, { "sub_cat": "Hydro Juicery", "items": [ { "name": "Cold Press Mix", "image": "/test_img/nmk14.png" }, { "name": "Mint Hydrate", "image": "/test_img/nmk14.png" }, { "name": "Fruit Amp", "image": "/test_img/nmk12.webp" }, ] }, { "sub_cat": "Flavour Filled Pots", "items": [ { "name": "Schezwan Pot Rice", "image": "/test_img/nmk14.jpeg" }, { "name": "Cream Noodle Mix", "image": "/test_img/nmk13.jpg" }, { "name": "Veg Bowl Spice", "image": "/test_img/nmk15.webp" }, ] }, { "sub_cat": "Ultra Crunch Snacks", "items": [ { "name": "Salted Chip Mix", "image": "/test_img/nmk14.png" }, { "name": "Basil Nibbles", "image": "/test_img/nmk12.webp" }, { "name": "Lemon Salt Crisp", "image": "/test_img/nmk15.webp" }, { "name": "Rock Salt Crackers", "image": "/test_img/nmk13.jpg" }, ] }, ] }, { "id": 5, "type": "category_grid", "title": "🥤 Best of the Week — Mega Save", "color_theme_name":'fresh vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Quick Meal Pots", "items": [ { "name": "Teriyaki Rice", "image": "/test_img/nmk14.jpeg" }, { "name": "Soy Noodles", "image": "/test_img/nmk15.webp" }, { "name": "Curry Pot Bites", "image": "/test_img/nmk13.jpg" }, ] }, { "sub_cat": "Juice Factory", "items": [ { "name": "Mixed Orange", "image": "/test_img/nmk12.webp" }, { "name": "Fruit Rush", "image": "/test_img/nmk14.png" }, { "name": "Berry Lime", "image": "/test_img/nmk14.jpeg" }, { "name": "Tangy Mojito", "image": "/test_img/nmk13.jpg" }, ] }, { "sub_cat": "Cheese Oven Crust", "items": [ { "name": "Double Layer Crust", "image": "/test_img/nmk15.webp" }, { "name": "Vegan Slice", "image": "/test_img/nmk14.png" }, { "name": "Giant Slice", "image": "/test_img/nmk14.jpeg" }, ] }, ] }, { "id": 10, "type": "category_grid", "title": "🍱 Most Searched", "color_theme_name":'discover vibe', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Households", "items": [ { "name": "Noodles", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk6.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk10.jpeg" }, { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/bs2.webp" }, { "name": "Pizza", "image": "/test_img/bs2.webp" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, { "name": "Juices", "image": "/test_img/nmk9.webp" }, ], }, { "sub_cat": "Households", "items": [ { "name": "Noodles", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk6.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk10.jpeg" }, { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/bs2.webp" }, { "name": "Pizza", "image": "/test_img/bs2.webp" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, { "name": "Juices", "image": "/test_img/nmk9.webp" }, ], }, { "sub_cat": "Households", "items": [ { "name": "Noodles", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk6.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk10.jpeg" }, { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/bs2.webp" }, { "name": "Pizza", "image": "/test_img/bs2.webp" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, { "name": "Juices", "image": "/test_img/nmk9.webp" }, ], } ] }, { "id": 11, "type": "category_grid", "title": "🍱 Get upto 70% off || Deals Perfect for You", "color_theme_name":'woman fav', "gridCol": 3, "overflowX": False, "items": [ { "sub_cat": "Households", "items": [ { "name": "Noodles", "image": "/test_img/nmk12.webp" }, { "name": "Pizza", "image": "/test_img/nmk13.jpg" }, { "name": "Juices", "image": "/test_img/nmk14.jpeg" }, { "name": "Pizza", "image": "/test_img/nmk14.jpeg" }, { "name": "Juices", "image": "/test_img/nmk14.png" }, { "name": "Juices", "image": "/test_img/nmk15.webp" }, ], }, ], }, 
        ]
        return Response(sections)
    
    
from .models import Form, FormResponse, FormAnswer
from .serializers import FormSerializer

class FormViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    # GET /forms/<id>/
    def retrieve(self, request, pk=None):
        try:
            form = Form.objects.get(id=pk)
        except Form.DoesNotExist:
            return Response({"error": "Form Not Found"}, status=404)

        return Response(FormSerializer(form).data)

    # POST /forms/
    def create(self, request):
        serializer = FormSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            form = serializer.save()
            return Response({"id": form.id}, status=201)
        return Response(serializer.errors, status=400)

    # POST /forms/<id>/submit/
    @action(methods=['post'], detail=True)
    def submit(self, request, pk=None):
        try:
            form = Form.objects.get(id=pk)
        except Form.DoesNotExist:
            return Response({"error": "Form Not Found"}, status=404)

        response = FormResponse.objects.create(form=form)

        for ans in request.data.get("answers", []):
            FormAnswer.objects.create(
                response=response,
                field_id=ans["field"],
                value=ans["value"]
            )

        return Response({"message": "Submitted"}, status=201)

