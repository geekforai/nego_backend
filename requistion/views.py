from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequisitionSerializer
import os
from django.conf import settings
class RequisitionCreateView(APIView):

    def post(self, request):
        serializer = RequisitionSerializer(data=request.data)
        if serializer.is_valid():
            instance=serializer.save()
            self.save_rfq_to_txt(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def save_rfq_to_txt(self, rfq_instance):
        rfq_data = (
            f"Product Name: {rfq_instance.product_name}\n"
            f"Delivery Date: {rfq_instance.delivery_date}\n"
            f"Negotiation Closure Date: {rfq_instance.negotiation_closure_date}\n"
            f"Type of Currency: {rfq_instance.type_of_currency}\n"
            f"Target Price: {rfq_instance.target_price}\n"
            f"Total Price: {rfq_instance.total_price}\n"
            f"Payment Terms: {rfq_instance.payment_terms}\n"
            f"Status: {rfq_instance.status}\n"
            f"Created By: {rfq_instance.created_by}\n"
        )

        # Define the file path
        file_path = os.path.join(settings.MEDIA_ROOT,'static','RFQs', f'rfq_{rfq_instance.id}.txt')

        # Write to the text file
        with open(file_path, 'w') as file:
            file.write(rfq_data)

