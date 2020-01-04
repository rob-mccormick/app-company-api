from rest_framework import serializers

from core.models import CbJobsData, CbQnsData


class CbJobsDataCreateSerializer(serializers.ModelSerializer):
    """Serilizer to create chatbot job data objects"""

    class Meta:
        model = CbJobsData
        exclude = ("company",)


class CbQnsDataCreateSerializer(serializers.ModelSerializer):
    """Serializer to create chatbot question data objects"""

    class Meta:
        model = CbQnsData
        exclude = ("company",)
