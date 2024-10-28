from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'  # Include all fields in the model
        read_only_fields = ['chat_id', 'created_at', 'created_by']  # Make certain fields read-only
