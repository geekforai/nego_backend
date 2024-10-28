from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
import json
from .serializers import ChatMessageSerializer
from langchain_community.document_loaders.text import TextLoader
from message.LLM import getChain
from message.PostLLM import getPostChain
import os
from django.conf import settings
from langchain_core.messages import AIMessage, HumanMessage
from chat.models import Chat
from requistion.models import Requisition
from django.http import StreamingHttpResponse
import json
from message.models import ChatMessage
from rest_framework.exceptions import NotFound
class ChatMessageCreateView(APIView):
    def post(self, request):
        try:
            # Validate incoming data
            serializer = ChatMessageSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                history=self.get_history(instance.chat_id)
                # Load strategy and create the chain
                
                chain = getChain()
                # Load the context from the text file
                text_loader = TextLoader(
                    os.path.join(settings.MEDIA_ROOT, 'static', 'RFQs', f'rfq_{Chat.objects.get(chat_id=instance.chat_id).requisition.id}.txt')
                )
                context = text_loader.load()
                def generate_response():
                    print('******************')
                    full_response=''
                    for chunk in chain.stream(input={'chat_history':history, 'input':instance.message_text, 'context':context}):
                        print(chunk.keys())
                        if 'answer' in chunk.keys():
                            full_response=full_response+chunk['answer']
                            yield chunk['answer']
                        else:
                            yield ''
                    bot_serializer = ChatMessageSerializer(data={'message_text':full_response,'message_type':'bot','chat':instance.chat_id}) 
                    if bot_serializer.is_valid():
                        final_data=bot_serializer.save()
                        yield final_data
                    print('******************')
                # Create the StreamingHttpResponse
                response = StreamingHttpResponse(generate_response(), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="yourmodel_data.json"'
                response['Cache-Control'] = 'no-cache'  # Disable caching
                response['Pragma'] = 'no-cache'         # Additional cache control
                return response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_history(self,chat_id):
        history=[]
        for data in ChatMessage.objects.filter(chat_id=chat_id).order_by('created_at'):
            if data.message_type=='user':
                history.append(HumanMessage(content=data.message_text))
            else:
                history.append(AIMessage(content=data.message_text))
        return history
    
class MessageFeedbackCreateView(APIView):
    def post(self, request):
            id = request.data.get('message_id')  # Use request.data to access POST data
            feedback = request.data.get('feedback')
            errors = {}
            if id is None:
                errors['message_id'] = "'message_id' is required."
            if feedback is None:
                errors['feedback'] = "'feedback' is required."
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            # Validate input
            if id is None or feedback is None:
                return Response({"error": "chat_id and feedback are required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Fetch the chat object
                message = ChatMessage.objects.get(id=id)
                message.feedback = feedback
                message.save()
                # Serialize the updated chat object
                serializer = ChatMessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Chat.DoesNotExist:
                raise NotFound({"error": "Chat not found."})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostChatMessageCreateView(APIView):
    def post(self, request):
        try:
            # Validate incoming data
            serializer = ChatMessageSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                history=self.get_history(instance.chat_id)
                print(history)
                chain = getPostChain()
                # Load the context from the text file
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'static', 'RFQ_Benchmarks', f'rfq_{Chat.objects.get(chat_id=instance.chat_id).requisition.id}.txt')):
                    return Response({'status':"inactive"}, status=status.HTTP_204_NO_CONTENT)
                text_loader = TextLoader(
                    os.path.join(settings.MEDIA_ROOT, 'static', 'RFQs', f'RFQ_Benchmarks{Chat.objects.get(chat_id=instance.chat_id).requisition.id}.txt')
                )
                context = text_loader.load()
                def generate_response():
                    print('******************')
                    full_response=''
                    for chunk in chain.stream(input={'chat_history':history, 'input':instance.message_text, 'context':context}):
                        print(chunk.keys())
                        if 'answer' in chunk.keys():
                            full_response=full_response+chunk['answer']
                            yield chunk['answer']
                        else:
                            yield ''
                    bot_serializer = ChatMessageSerializer(data={'message_text':full_response,'message_type':'bot','chat':instance.chat_id}) 
                    if bot_serializer.is_valid():
                        final_data=bot_serializer.save()
                        yield final_data
                # Create the StreamingHttpResponse
                response = StreamingHttpResponse(generate_response(), content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="yourmodel_data.json"'
                response['Cache-Control'] = 'no-cache'  # Disable caching
                response['Pragma'] = 'no-cache'         # Additional cache control
                return response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_history(self,chat_id):
        history=[]
        for data in ChatMessage.objects.filter(chat_id=chat_id).order_by('created_at'):
            if data.message_type=='user':
                history.append(HumanMessage(content=data.message_text))
            else:
                history.append(AIMessage(content=data.message_text))
        return history
    
class PostMessageFeedbackCreateView(APIView):
    def post(self, request):
            id = request.data.get('message_id')  # Use request.data to access POST data
            feedback = request.data.get('feedback')
            errors = {}
            if id is None:
                errors['message_id'] = "'message_id' is required."
            if feedback is None:
                errors['feedback'] = "'feedback' is required."
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            # Validate input
            if id is None or feedback is None:
                return Response({"error": "chat_id and feedback are required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                # Fetch the chat object
                message = ChatMessage.objects.get(id=id)
                message.feedback = feedback
                message.save()
                # Serialize the updated chat object
                serializer = ChatMessageSerializer(message)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Chat.DoesNotExist:
                raise NotFound({"error": "Chat not found."})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
