from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from .models import Lead
from .serializers import (
   LeadSerializer
)
from .permissions import IsSeller
from food99api.models import BuyerProfile
from sellers.models import Seller
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# -------------------------
# LEAD CRUD
# -------------------------
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]
    
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['buyer__user__username']
    
    def perform_create(self, serializer):
        serializer.save(buyer=BuyerProfile.objects.get(user=self.request.user))
    
    def get_queryset(self):
        print("QQQSET:", self.request.user)
        return Lead.objects.filter(seller=Seller.objects.get(user=self.request.user)).exclude( status="new")
    
    # @action(detail=True, methods=['GET'], permission_classes=[permissions.IsAuthenticated, IsSeller])
    # def F_(self, request, pk=None):
    #     filter_=pk
    #     FILTER = {"n_":"new", "ctd_":"contacted"}
    #     if filter_ not in FILTER:
    #         raise Response({"NOT FOUND": filter_}, status=404)
    #     value = FILTER[filter_]
    #     leads_queryset = Lead.objects.filter(status=value)
    #     serializer = LeadSerializer(
    #         leads_queryset,
    #         many=True,
    #         context={"request":request}            
    #     )
    #     return Response(serializer.data)
              

        