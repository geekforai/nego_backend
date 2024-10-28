
from background_task import background
from chat.models import Chat
from chat.seializers import ChatSerializer
from langchain_core.messages import AIMessage, HumanMessage
from message.models import ChatMessage
def get_history(chat_id):
        history=[]
        for data in ChatMessage.objects.filter(chat_id=chat_id).order_by('created_at'):
            if data.message_type=='user':
                history.append(HumanMessage(content=data.message_text))
            else:
                history.append(AIMessage(content=data.message_text))
        return history
@background(schedule=5)  # Runs after 60 seconds
def send_welcome_email(requisition_instance):
    chat_ids = [chat.chat_id for chat in Chat.objects.filter(requisition_id=requisition_instance)]
    histories=[get_history(chat_id=chat_id) for chat_id in chat_ids]
    print(histories)
    
    