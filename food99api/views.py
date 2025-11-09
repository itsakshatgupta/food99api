from rest_framework import viewsets, permissions, generics
from django.contrib.auth.models import User
from .models import Seller, Product, BuyerProfile, Message, Lead
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    UserSerializer, SellerSerializer, ProductSerializer,
    BuyerProfileSerializer, MessageSerializer, LeadSerializer, RegisterSerializer
)



# ------------------- REGISTER USER -------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ------------------- BUYER CRUD -------------------
class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- User (for info only) ---
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# --- Seller ---
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all().order_by('-joined_on')
    serializer_class = SellerSerializer
    permission_classes = [permissions.AllowAny]


# --- Product ---
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# --- Buyer ---
class BuyerProfileViewSet(viewsets.ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [permissions.AllowAny]


# --- Message ---
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]


# --- Lead ---
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.AllowAny]

from rest_framework.views import APIView
from rest_framework.response import Response

class HomeSectionsView(APIView):
    def get(self, request):
        sections = [
        {
            "id": 1,
            "type": "offers",
            "title": "🔥 Offers for You",
            "gridCol": 2,
            "color_theme_name": 'fresh vibe',
            "overflowX": False,
            "items": [
                { "title": "50% OFF on First Order", "code": "WELCOME50", "image": "/test_img/nmk5.jpg", "bg": "bg-gradient-to-r from-blue-500 to-indigo-500" },
                { "title": "Free Delivery Above ₹199", "code": "FREESHIP", "image": "/test_img/nmk2.png", "bg": "bg-gradient-to-r from-green-400 to-emerald-500" },
                { "title": "10% Cashback via UPI", "code": "UPI10", "image": "/test_img/nmk3.jpeg", "bg": "bg-gradient-to-r from-rose-400 to-pink-500" },
                { "title": "Flat ₹75 OFF for Students", "code": "STUDENT75", "image": "/test_img/nmk4.jpg", "bg": "bg-gradient-to-r from-amber-400 to-orange-500" },
            ],
        },
        {
            "id": 2,
            "type": "category_grid",
            "title": "🍱 Popular Categories",
            "color_theme_name": 'focus vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Clothes", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk3.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk4.jpg" },
                        { "name": "Juices", "image": "/test_img/nmk7.jpeg" },
                    ],
                },
                {
                    "sub_cat": "Foods", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk3.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk4.jpg" },
                        { "name": "Juices", "image": "/test_img/nmk7.jpeg" },
                    ],
                },
                {
                    "sub_cat": "Households", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk3.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk4.jpg" },
                        { "name": "Juices", "image": "/test_img/nmk7.jpeg" },
                    ],
                },
            ],
        },
        {
            "id": 3,
            "type": "search_suggestion",
            "title": "Are you looking these?",
            "gridCol": 2,
            "overflowX": False,
            "items": [
                { "name": "Hakka Noodles", "image": "/test_img/nmk5.jpg", "api": "/api/menu/trending" },
                { "name": "Pizza Sauce", "image": "/test_img/nmk4.jpg", "api": "/api/menu/trending" },
                { "name": "Healthy Juices", "image": "/test_img/nmk7.jpeg", "api": "/api/menu/trending" },
            ],
        },
        {
            "id": 5,
            "type": "product_grid",
            "title": "🍱 Featured Products",
            "gridCol": False,
            "overflowX": True,
            "items": [
                { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                { "name": "Juices", "image": "/test_img/nmk14.jpeg" },
                { "name": "Pizza", "image": "/test_img/nmk14.jpeg" },
                { "name": "Juices", "image": "/test_img/nmk14.png" },
                { "name": "Juices", "image": "/test_img/nmk15.webp" },
                { "name": "Pizza", "image": "/test_img/bs2.webp" },
                { "name": "Juices", "image": "/test_img/bs1.webp" },
            ],
        },
        {
            "id": 1,
            "type": "category_grid",
            "title": "🔥 Up to 70% Off — Deal Festival",
            "color_theme_name": 'discover vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Gourmet Snacks", "items": [
                        { "name": "Sesame Crackers", "image": "/test_img/nmk13.jpg" },
                        { "name": "Rice Chips", "image": "/test_img/nmk15.webp" },
                        { "name": "Oat Bites", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Coconut Crisps", "image": "/test_img/nmk12.webp" },
                        { "name": "Cumin Sticks", "image": "/test_img/nmk14.png" },
                    ]
                },
                {
                    "sub_cat": "Hydration Essentials", "items": [
                        { "name": "Vitamin Water", "image": "/test_img/nmk14.png" },
                        { "name": "Energy Sipper", "image": "/test_img/nmk12.webp" },
                        { "name": "Aloe Booster", "image": "/test_img/nmk15.webp" },
                    ]
                },
                {
                    "sub_cat": "Pizzeria Favourites", "items": [
                        { "name": "Thin Crust Slice", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Cheese Burst", "image": "/test_img/nmk14.png" },
                        { "name": "NYC Lava Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Mushroom Special", "image": "/test_img/nmk15.webp" },
                    ]
                }, {
                    "sub_cat": "Gourmet Snacks", "items": [
                        { "name": "Sesame Crackers", "image": "/test_img/nmk13.jpg" },
                        { "name": "Rice Chips", "image": "/test_img/nmk15.webp" },
                        { "name": "Oat Bites", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Coconut Crisps", "image": "/test_img/nmk12.webp" },
                        { "name": "Cumin Sticks", "image": "/test_img/nmk14.png" },
                    ]
                },
                {
                    "sub_cat": "Hydration Essentials", "items": [
                        { "name": "Vitamin Water", "image": "/test_img/nmk14.png" },
                        { "name": "Energy Sipper", "image": "/test_img/nmk12.webp" },
                        { "name": "Aloe Booster", "image": "/test_img/nmk15.webp" },
                    ]
                },
                {
                    "sub_cat": "Pizzeria Favourites", "items": [
                        { "name": "Thin Crust Slice", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Cheese Burst", "image": "/test_img/nmk14.png" },
                        { "name": "NYC Lava Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Mushroom Special", "image": "/test_img/nmk15.webp" },
                    ]
                },
            ]
        },
        {
            "id": 2,
            "type": "category_grid",
            "title": "🍱 Grab More — Pay Less",
            "color_theme_name": 'fresh vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Asian Bites", "items": [
                        { "name": "Ramen Bowl", "image": "/test_img/nmk12.webp" },
                        { "name": "Cheese Pot Rice", "image": "/test_img/nmk15.webp" },
                        { "name": "Bok Spice Plate", "image": "/test_img/nmk14.png" },
                    ]
                },
                {
                    "sub_cat": "Energy Boosters", "items": [
                        { "name": "Guava Boost", "image": "/test_img/nmk13.jpg" },
                        { "name": "Lychee Rush", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Mango Power", "image": "/test_img/nmk12.webp" },
                        { "name": "Berry Aminos", "image": "/test_img/nmk14.png" },
                    ]
                },
                {
                    "sub_cat": "Baked Specials", "items": [
                        { "name": "Stuffed Pizza", "image": "/test_img/nmk14.png" },
                        { "name": "Napoli Slice", "image": "/test_img/nmk13.jpg" },
                        { "name": "NYC Square", "image": "/test_img/nmk15.webp" },
                    ]
                },
                {
                    "sub_cat": "Instant Heat Meals", "items": [
                        { "name": "Butter Corn Bowl", "image": "/test_img/nmk13.jpg" },
                        { "name": "Hot Noodles", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Spice Mix Pot", "image": "/test_img/nmk12.webp" },
                    ]
                },
            ]
        },
        {
            "id": 5,
            "type": "product_grid",
            "title": "🍱 Featured Products",
            "gridCol": False,
            "overflowX": True,
            "items": [
                { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                { "name": "Juices", "image": "/test_img/nmk14.jpeg" },
                { "name": "Pizza", "image": "/test_img/nmk14.jpeg" },
                { "name": "Juices", "image": "/test_img/nmk14.png" },
                { "name": "Juices", "image": "/test_img/nmk15.webp" },
                { "name": "Pizza", "image": "/test_img/bs2.webp" },
                { "name": "Juices", "image": "/test_img/bs1.webp" },
            ],
        },
        {
            "id": 3,
            "type": "category_grid",
            "title": "🥡 Deal Fiesta — Max Saver Combo",
            "color_theme_name": 'woman fav',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Italian Crust House", "items": [
                        { "name": "Roman Crust", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Cheese Overload", "image": "/test_img/nmk13.jpg" },
                        { "name": "Firewood Slice", "image": "/test_img/nmk12.webp" },
                        { "name": "Garlic Toppings", "image": "/test_img/nmk15.webp" },
                    ]
                },
                {
                    "sub_cat": "Refreshing Shots", "items": [
                        { "name": "Mint Lime", "image": "/test_img/nmk14.png" },
                        { "name": "Kiwi Boost", "image": "/test_img/nmk15.webp" },
                        { "name": "Lemon Chill", "image": "/test_img/nmk12.webp" },
                        { "name": "Berry Punch", "image": "/test_img/nmk14.jpeg" },
                    ]
                },
                {
                    "sub_cat": "Asian Pot Flare", "items": [
                        { "name": "Soba Noodles", "image": "/test_img/nmk14.png" },
                        { "name": "Korean Spicy", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Thai Crack Mix", "image": "/test_img/nmk13.jpg" },
                    ]
                },
            ]
        },
        {
            "id": 4,
            "type": "category_grid",
            "title": "🍕 Crazy Combo Drop — Deal Bomb",
            "color_theme_name": 'discover vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Fusion Slices", "items": [
                        { "name": "Volcano Slice", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Hot Pepperoni", "image": "/test_img/nmk15.webp" },
                        { "name": "Smoked Special", "image": "/test_img/nmk13.jpg" },
                        { "name": "BBQ Deluxe", "image": "/test_img/nmk12.webp" },
                    ]
                },
                {
                    "sub_cat": "Hydro Juicery", "items": [
                        { "name": "Cold Press Mix", "image": "/test_img/nmk14.png" },
                        { "name": "Mint Hydrate", "image": "/test_img/nmk14.png" },
                        { "name": "Fruit Amp", "image": "/test_img/nmk12.webp" },
                    ]
                },
                {
                    "sub_cat": "Flavour Filled Pots", "items": [
                        { "name": "Schezwan Pot Rice", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Cream Noodle Mix", "image": "/test_img/nmk13.jpg" },
                        { "name": "Veg Bowl Spice", "image": "/test_img/nmk15.webp" },
                    ]
                },
                {
                    "sub_cat": "Ultra Crunch Snacks", "items": [
                        { "name": "Salted Chip Mix", "image": "/test_img/nmk14.png" },
                        { "name": "Basil Nibbles", "image": "/test_img/nmk12.webp" },
                        { "name": "Lemon Salt Crisp", "image": "/test_img/nmk15.webp" },
                        { "name": "Rock Salt Crackers", "image": "/test_img/nmk13.jpg" },
                    ]
                },
            ]
        },
        {
            "id": 5,
            "type": "category_grid",
            "title": "🥤 Best of the Week — Mega Save",
            "color_theme_name": 'fresh vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Quick Meal Pots", "items": [
                        { "name": "Teriyaki Rice", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Soy Noodles", "image": "/test_img/nmk15.webp" },
                        { "name": "Curry Pot Bites", "image": "/test_img/nmk13.jpg" },
                    ]
                },
                {
                    "sub_cat": "Juice Factory", "items": [
                        { "name": "Mixed Orange", "image": "/test_img/nmk12.webp" },
                        { "name": "Fruit Rush", "image": "/test_img/nmk14.png" },
                        { "name": "Berry Lime", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Tangy Mojito", "image": "/test_img/nmk13.jpg" },
                    ]
                },
                {
                    "sub_cat": "Cheese Oven Crust", "items": [
                        { "name": "Double Layer Crust", "image": "/test_img/nmk15.webp" },
                        { "name": "Vegan Slice", "image": "/test_img/nmk14.png" },
                        { "name": "Giant Slice", "image": "/test_img/nmk14.jpeg" },
                    ]
                },
            ]
        },


        {
            "id": 10,
            "type": "category_grid",
            "title": "🍱 Most Searched",
            "color_theme_name": 'discover vibe',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Households", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk14.png" },
                        { "name": "Juices", "image": "/test_img/nmk6.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk10.jpeg" },
                        { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                        { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Juices", "image": "/test_img/bs2.webp" },
                        { "name": "Pizza", "image": "/test_img/bs2.webp" },
                        { "name": "Juices", "image": "/test_img/nmk15.webp" },
                        { "name": "Juices", "image": "/test_img/nmk9.webp" },
                    ],
                }, {
                    "sub_cat": "Households", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk14.png" },
                        { "name": "Juices", "image": "/test_img/nmk6.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk10.jpeg" },
                        { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                        { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Juices", "image": "/test_img/bs2.webp" },
                        { "name": "Pizza", "image": "/test_img/bs2.webp" },
                        { "name": "Juices", "image": "/test_img/nmk15.webp" },
                        { "name": "Juices", "image": "/test_img/nmk9.webp" },
                    ],
                }, {
                    "sub_cat": "Households", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk14.png" },
                        { "name": "Juices", "image": "/test_img/nmk6.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk10.jpeg" },
                        { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                        { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Juices", "image": "/test_img/bs2.webp" },
                        { "name": "Pizza", "image": "/test_img/bs2.webp" },
                        { "name": "Juices", "image": "/test_img/nmk15.webp" },
                        { "name": "Juices", "image": "/test_img/nmk9.webp" },
                    ],
                }
            ]
        },
        {
            "id": 11,
            "type": "category_grid",
            "title": "🍱 Get upto 70% off || Deals Perfect for You",
            "color_theme_name": 'woman fav',
            "gridCol": 3,
            "overflowX": False,
            "items": [
                {
                    "sub_cat": "Households", "items": [
                        { "name": "Noodles", "image": "/test_img/nmk12.webp" },
                        { "name": "Pizza", "image": "/test_img/nmk13.jpg" },
                        { "name": "Juices", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Pizza", "image": "/test_img/nmk14.jpeg" },
                        { "name": "Juices", "image": "/test_img/nmk14.png" },
                        { "name": "Juices", "image": "/test_img/nmk15.webp" },
                    ],
                },
            ],
        },
    ]
        return Response(sections)
