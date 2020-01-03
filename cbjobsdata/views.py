from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework_api_key.permissions import HasAPIKey

from core.models import CbJobsData, Company

from cbjobsdata.serializers import CbJobsDataCreateSerializer


class CbJobsDataCreateView(generics.CreateAPIView):
    """View to create new job data objects in the database"""
    queryset = CbJobsData.objects.all()
    serializer_class = CbJobsDataCreateSerializer
    permission_classes = (HasAPIKey,)

    def perform_create(self, serializer):
        """Over-rides the default perform_create as using ForeignKey"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        serializer.save(company=company)
