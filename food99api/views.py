from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MenuItem, Cart
from .serializers import MenuItemSerializer, CartSerializer

# Create your views here.
from django.http import HttpResponse
from .models import Category
from .serializers import CategorySerializer

def home(request):
    return HttpResponse("Hello, Akshat! Django is running.")

@api_view(['GET'])
def menu_by_category(request):
    categories = Category.objects.prefetch_related('items').all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem

@api_view(['GET'])
def menu_items(request):
    data = list(MenuItem.objects.values())
    return Response(data)


