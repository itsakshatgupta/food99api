from rest_framework import serializers
from .models import Lead

# -------------------------
# LEAD SERIALIZER
# -------------------------
class LeadSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    # seller = serializers.CharField(source='seller.id', read_only=True)
    buyer = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    
    product_id = serializers.IntegerField(write_only=True)
    seller_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Lead
        fields = '__all__'
    
    def get_product(self, obj):
        return {"id":obj.product.id, "name":obj.product.name}
    
    def get_buyer(self, obj):
        return {"name":obj.buyer.user.username,"connect":obj.buyer.whatsapp_number or obj.buyer.user.phone,"location":obj.buyer.user.location or "Not Provided"}
    
    def get_priority(self, obj):
        return "Medium"
        
   