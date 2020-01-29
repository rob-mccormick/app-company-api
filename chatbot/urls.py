from django.urls import path

from chatbot.views import CompanyChatbotView


app_name = 'chatbot'

urlpatterns = [
    path('companychatbot/get',
        CompanyChatbotView.as_view(),
        name='companychatbot-list'
    ),
]
