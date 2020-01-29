from rest_framework import generics
from rest_framework.generics import get_object_or_404

from rest_framework_api_key.permissions import HasAPIKey

from core.models import CompanyChatbot, Company, User

from chatbot.serializers import CompanyChatbotSerializer


class CompanyChatbotView(generics.ListAPIView):
    """Base view set for getting company chatbot objects from the database"""
    queryset = CompanyChatbot.objects.all()
    serializer_class = CompanyChatbotSerializer
    permission_classes = (HasAPIKey,)

    def get_queryset(self):
        """Return object for the current authenticated company only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(companychatbot__isnull=False)

        return queryset.filter(company=self.request.company)
