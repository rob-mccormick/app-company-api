from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework_api_key.permissions import HasAPIKey

from core.models import CbJobsData, CbQnsData, CbBrowsingData, Company

from cbdata.serializers import CbJobsDataCreateSerializer, \
                               CbQnsDataCreateSerializer, \
                               CbBrowsingDataCreateSerializer


class BasicCbDataCreateView(generics.CreateAPIView):
    """Base view set for creating new chatbot data objects in the database"""
    permission_classes = (HasAPIKey,)

    def perform_create(self, serializer):
        """Over-rides the default perform_create as using ForeignKey"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        serializer.save(company=company)


class CbJobsDataCreateView(BasicCbDataCreateView):
    """Create new chatbot job data objects in the database"""
    queryset = CbJobsData.objects.all()
    serializer_class = CbJobsDataCreateSerializer


class CbQnsDataCreateView(BasicCbDataCreateView):
    """Create new chatbot quetion data objects in the database"""
    queryset = CbQnsData.objects.all()
    serializer_class = CbQnsDataCreateSerializer


class CbBrowsingDataCreateView(BasicCbDataCreateView):
    """Create new chatbot quetion data objects in the database"""
    queryset = CbBrowsingData.objects.all()
    serializer_class = CbBrowsingDataCreateSerializer
