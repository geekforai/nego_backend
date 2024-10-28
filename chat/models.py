import random
import string
from django.db import models
from django.contrib.auth.models import User
from requistion.models import Requisition
class Chat(models.Model):
    chat_id = models.CharField(max_length=12, unique=True, editable=False,primary_key=True)
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    feedback=models.TextField(default=None,null=True)
    created_by = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.chat_id:
            self.chat_id = self.generate_chat_id()
        super().save(*args, **kwargs)

    def generate_chat_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def __str__(self):
        return self.chat_id
