from rest_framework import serializers

from core.models import CbJobsData, CbQnsData, CbBrowsingData


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


class CbBrowsingDataCreateSerializer(serializers.ModelSerializer):
    """Serializer to create chatbot browsing data objects"""

    class Meta:
        model = CbBrowsingData
        exclude = ("company",)
