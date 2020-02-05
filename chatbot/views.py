from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework_api_key.permissions import HasAPIKey

from core.models import Benefit, Company, CompanyChatbot, Job, JobMap, \
                        Location, Question

from chatbot.serializers import BenefitSerializer, CompanyChatbotSerializer, \
                                JobSerializer, JobMapSerializer, \
                                LocationSerializer, QuestionSerializer


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

        return queryset.filter(company=company, active_benefit=True)


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


class JobView(generics.ListAPIView):
    """Base view set for getting job objects from the database"""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return active objects for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        # return queryset.filter(company=company)
        return queryset.filter(company=company, active_job=True)


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


class QuestionView(generics.ListAPIView):
    """Base view set for getting question objects from the database"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        company_pk = self.kwargs.get("company_pk")
        company = get_object_or_404(Company, pk=company_pk)

        queryset = self.queryset

        return queryset.filter(company=company, active_question=True)
