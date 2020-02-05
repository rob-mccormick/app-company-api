from django.urls import path

from chatbot.views import BenefitView, CompanyChatbotView, JobView, \
                          JobMapView, LocationView, QuestionView


app_name = 'chatbot'

urlpatterns = [
    path(
        'benefit/<int:company_pk>',
        BenefitView.as_view(),
        name='benefit-list'
    ),
    path(
        'companychatbot/<int:company_pk>',
        CompanyChatbotView.as_view(),
        name='companychatbot-list'
    ),
    path(
        'job/<int:company_pk>',
        JobView.as_view(),
        name='job-list'
    ),
    path(
        'jobmap/<int:company_pk>',
        JobMapView.as_view(),
        name='jobmap-list'
    ),
    path(
        'location/<int:company_pk>',
        LocationView.as_view(),
        name='location-list'
    ),
    path(
        'question/<int:company_pk>',
        QuestionView.as_view(),
        name='question-list'
    ),
]
