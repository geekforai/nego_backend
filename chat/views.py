from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Requisition
from .seializers import ChatSerializer
from rest_framework.exceptions import NotFound

class ChatCreateView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Set the created_by field
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChatFeedbackCreateView(APIView):
    def post(self, request):
        chat_id = request.data.get('chat_id')  # Use request.data to access POST data
        feedback = request.data.get('feedback')
        errors = {}
        if chat_id is None:
            errors['chat_id'] = "'chat_id' is required."
        if feedback is None:
            errors['feedback'] = "'feedback' is required."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Validate input
        if chat_id is None or feedback is None:
            return Response({"error": "chat_id and feedback are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the chat object
            chat = Chat.objects.get(chat_id=chat_id)
            chat.feedback = feedback
            chat.save()

            # Serialize the updated chat object
            serializer = ChatSerializer(chat)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Chat.DoesNotExist:
            raise NotFound({"error": "Chat not found."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
