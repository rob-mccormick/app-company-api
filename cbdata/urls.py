from django.urls import path

from cbdata.views import CbJobsDataCreateView


app_name = 'cbdata'

urlpatterns = [
    path(
        'cbjobsdata/<int:company_pk>/post',
        CbJobsDataCreateView.as_view(),
        name='cbjobsdata-create'
    ),
]
