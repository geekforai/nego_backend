from django.db import models
from chat.models import Chat
from datetime import datetime
class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    id = models.AutoField(primary_key=True)
    message_text = models.TextField()  # The text of the message
    message_type = models.CharField(max_length=4, choices=MESSAGE_TYPES)  # Type of message: user or bot
    chat= models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')  # Link to the Chat
    feed_back = models.TextField(blank=True, null=True)  # Feedback for the message
    created_at=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Message {self.id} in chat {self.chat.chat_id} from {self.message_type}"
