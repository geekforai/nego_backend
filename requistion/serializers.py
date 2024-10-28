from rest_framework import serializers
from .models import Requisition

class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        fields = '__all__'  # This will include all fields in the model
        
    def validate(self, attrs):
        # Custom validation can be added here if needed
        return attrs
