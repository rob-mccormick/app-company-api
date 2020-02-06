from django.urls import path

from cbdata.views import CbJobsDataCreateView, CbQnsDataCreateView, \
                         CbBrowsingDataCreateView


app_name = 'cbdata'

urlpatterns = [
    path(
        'cbjobsdata/<uuid:company_pk>/post',
        CbJobsDataCreateView.as_view(),
        name='cbjobsdata-create'
    ),
    path(
        'cbqnsdata/<uuid:company_pk>/post',
        CbQnsDataCreateView.as_view(),
        name='cbqnsdata-create'
    ),
    path(
        'cbbrowsingdata/<uuid:company_pk>/post',
        CbBrowsingDataCreateView.as_view(),
        name='cbbrowsingdata-create'
    ),
]
