"""
URL configuration for nego_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from requistion.views import RequisitionCreateView
from chat.views import ChatCreateView,ChatFeedbackCreateView
from message.views import ChatMessageCreateView,MessageFeedbackCreateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('requisition/',RequisitionCreateView.as_view()),
    path('chat/',ChatCreateView.as_view()),
    path('chat-message/', ChatMessageCreateView.as_view(), name='chat-message-create'),
    path('chat-feedback/', ChatFeedbackCreateView.as_view() ),
    path('chat-message-feedback/', MessageFeedbackCreateView.as_view() ),
]
