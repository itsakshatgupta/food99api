import json
import uuid
import requests
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from .models import Cart, CartItem, MenuItem, CustomUser, Category, Order
from .serializers import CartSerializer, CartItemSerializer, CategorySerializer, SignupSerializer, CustomUserSerializer, OrderSerializer


CASHFREE_BASE_URL = "https://api.cashfree.com/pg"  # use sandbox for testing

@method_decorator(csrf_exempt, name='dispatch')

class CreateOrderView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(request.user)
        print('ss', serializer.data)
        order_id = str(uuid.uuid4())
        amount = request.data.get("amount", 1)  # you can calculate from cart
        
        headers = {
            "accept": "application/json",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2022-09-01",
            "Content-Type": "application/json",
        }

        payload = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": "cust_" + str(uuid.uuid4()),
                "customer_email": 'akshatguptatom@gmail.com',
                "customer_phone": '+918881316612',
            },
            "payment_method": { "upi": {
            "channel": "collect",
            "upi_id": "akshatguptatom@kotak"
        } }
            # "order_meta": {
            #     "payment_methods": "upi"  # 👈 restricts to UPI only
            # }
        }

        res = requests.post(f"{CASHFREE_BASE_URL}/orders", headers=headers, json=payload)

        return Response(res.json())
    
@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentView(APIView):
    # This view can be used as a webhook endpoint or for manual verification
    def post(self, request, *args, **kwargs):
        # For a webhook, you'd get the order_id from the request body
        order_id = request.data.get('order_id')

        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Make an API call to Cashfree to verify the payment status
        headers = {
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2022-01-01",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(f"{settings.CASHFREE_API_URL}/orders/{order_id}", headers=headers)
            response.raise_for_status()
            cashfree_data = response.json()

            payment_status = cashfree_data.get('order_status')

            # Update the order in your database based on the status
            try:
                order = Order.objects.get(order_id=order_id)
                if payment_status == 'PAID':
                    order.payment_status = 'COMPLETED'
                    # You can also clear the user's cart here
                    # cart = Cart.objects.get(user=order.user)
                    # cart.items.clear()
                else:
                    order.payment_status = payment_status
                order.save()

                return Response({'status': order.payment_status}, status=status.HTTP_200_OK)

            except Order.DoesNotExist:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        except requests.exceptions.RequestException as e:
            print(f"Cashfree API Verification Error: {e}")
            return Response({'error': 'Payment verification failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Include user data + tokens in response
        user_data = CustomUserSerializer(user).data
        return Response({
            "user": user_data,
            "refresh": str(refresh),
            "access": str(access)
        })


class CartItemViewSet(viewsets.ModelViewSet):
    """
    RESTful API for managing cart items
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        menu_item_id = request.data.get("menu_item_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update quantity of a cart item
        """
        try:
            cart_item = self.get_queryset().get(id=pk)
            print('cart;', cart_item)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = int(request.data.get("quantity", cart_item.quantity))
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Remove an item from cart
        """
        try:
            cart_item = self.get_queryset().get(id=pk)
            cart_item.delete()
            return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def mycart(self, request):
        """
        View entire cart with total
        """
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"items": [], "total": 0})

        serializer = CartSerializer(cart)
        items = []
        total = 0
    
        for cart_item in cart.cartitem_set.all():
            base_price = cart_item.menu_item.price
            line_total = base_price * cart_item.quantity
    
            items.append({
                "id": cart_item.id,
                "quantity": cart_item.quantity,
                "menu_item": {
                    "id": cart_item.menu_item.id,
                    "name": cart_item.menu_item.name,
                    "description": cart_item.menu_item.description,
                    "image": str(cart_item.menu_item.image.url) if cart_item.menu_item.image else None,
                    "price": str(base_price),
                    "variants": list(cart_item.menu_item.variant.values("id", "name", "price")),  # show all possible variants
                },
                "line_total": str(line_total),
            })
            total += line_total
    
        return Response({
            "items": items,
            "total": str(total),
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)

def home(request):
    return HttpResponse("Hello, Akshat! Django is running.")

@api_view(['GET'])
def menu_by_category(request):
    categories = Category.objects.prefetch_related('items').all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CartViewSet(request):
    print(request.user)
    cart = Cart.objects.get(user=CustomUser.objects.get(username=request.user))
    serializer = CartSerializer(cart)
    return Response(serializer.data)   # returns JSON

@api_view(['GET'])
def menu_items(request):
    data = list(MenuItem.objects.values())
    return Response(data)


