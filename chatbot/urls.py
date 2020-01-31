from django.urls import path

from chatbot.views import CompanyChatbotView


app_name = 'chatbot'

urlpatterns = [
    path(
        'companychatbot/<int:company_pk>',
        CompanyChatbotView.as_view(),
        name='companychatbot-list'
    ),
]
