from food99api.models import BuyerProfile
from django.db import models
from sellers.models import Seller, Product

class Lead(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    enquiry_text = models.TextField(blank=True)
    source = models.CharField(max_length=50, default='website')  # or 'whatsapp', 'call'
    status = models.CharField(
        max_length=20,
        choices=[('new', 'New'), ('contacted', 'Contacted'), ('closed', 'Closed')],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)
