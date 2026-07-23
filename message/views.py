from .serializers import MessageSerializer
from .models import Message
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

# -------------------------
# MESSAGE CRUD
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

