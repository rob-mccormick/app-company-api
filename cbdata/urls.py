from django.urls import path

from cbdata.views import CbJobsDataCreateView, CbQnsDataCreateView, \
                         CbBrowsingDataCreateView


app_name = 'cbdata'

urlpatterns = [
    path(
        'cbjobsdata/<int:company_pk>/post',
        CbJobsDataCreateView.as_view(),
        name='cbjobsdata-create'
    ),
    path(
        'cbqnsdata/<int:company_pk>/post',
        CbQnsDataCreateView.as_view(),
        name='cbqnsdata-create'
    ),
    path(
        'cbbrowsingdata/<int:company_pk>/post',
        CbBrowsingDataCreateView.as_view(),
        name='cbbrowsingdata-create'
    ),
]
