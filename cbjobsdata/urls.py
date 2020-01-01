from django.urls import path

from cbjobsdata.views import CbJobsDataCreateView


app_name = 'cbjobsdata'

urlpatterns = [
    path(
        'cbjobsdata/<int:company_pk>/post',
        CbJobsDataCreateView.as_view(),
        name='cbjobsdata-create'
    ),
]
