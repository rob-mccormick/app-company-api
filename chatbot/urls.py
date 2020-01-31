from django.urls import path

from chatbot.views import CompanyChatbotView, JobMapView


app_name = 'chatbot'

urlpatterns = [
    path(
        'companychatbot/<int:company_pk>',
        CompanyChatbotView.as_view(),
        name='companychatbot-list'
    ),
    path(
        'jobmap/<int:company_pk>',
        JobMapView.as_view(),
        name='jobmap-list'
    ),
]
