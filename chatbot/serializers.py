from rest_framework import serializers

from core.models import CompanyChatbot, JobMap, Benefit


class CompanyChatbotSerializer(serializers.ModelSerializer):
    """Serializer for CompanyChatbot objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CompanyChatbot
        fields = "__all__"


class JobMapSerializer(serializers.ModelSerializer):
    """Serializer for JobMap objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = JobMap
        fields = "__all__"


class BenefitSerializer(serializers.ModelSerializer):
    """Serializer for Benefit objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Benefit
        fields = "__all__"
