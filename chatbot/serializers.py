from rest_framework import serializers

from core.models import Benefit, CompanyChatbot, Job, JobMap, Location


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


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)
    location = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
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
