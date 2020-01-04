from rest_framework import serializers

from core.models import CbJobsData


class CbJobsDataCreateSerializer(serializers.ModelSerializer):
    """Serilizer to create chatbot job data objects"""

    class Meta:
        model = CbJobsData
        exclude = ("company",)
