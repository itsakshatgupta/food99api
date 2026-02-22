from django.db import models
from django.conf import settings
from sellers.models import Product

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    message_type = models.CharField(
        max_length=20,
        choices=[('text', 'Text'), ('image', 'Image'), ('enquiry', 'Enquiry')],
        default='text'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"
