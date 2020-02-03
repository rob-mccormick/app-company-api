from rest_framework import serializers

from core.models import Benefit, CompanyChatbot, JobMap, Location


class BenefitSerializer(serializers.ModelSerializer):
    """Serializer for Benefit objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Benefit
        fields = "__all__"


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


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Location
        fields = "__all__"
