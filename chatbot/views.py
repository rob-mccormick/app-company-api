from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework_api_key.permissions import HasAPIKey
# from core.permissions import HasCompanyAPIKey

from core.models import Benefit, Company, CompanyChatbot, JobMap, Location

from chatbot.serializers import BenefitSerializer, CompanyChatbotSerializer, \
                                JobMapSerializer, LocationSerializer


class BenefitView(generics.ListAPIView):
    """Base view set for getting benefit objects from the database"""
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        return queryset.filter(company=company)


class CompanyChatbotView(generics.ListAPIView):
    """Base view set for getting company chatbot objects from the database"""
    queryset = CompanyChatbot.objects.all()
    serializer_class = CompanyChatbotSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        return queryset.filter(company=company)


class JobMapView(generics.ListAPIView):
    """Base view set for getting jobmap objects from the database"""
    queryset = JobMap.objects.all()
    serializer_class = JobMapSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        return queryset.filter(company=company)


class LocationView(generics.ListAPIView):
    """Base view set for getting location objects from the database"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        return queryset.filter(company=company)
