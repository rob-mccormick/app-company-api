from rest_framework import serializers

from core.models import Benefit, CompanyChatbot, Job, JobMap, Location


class BenefitSerializer(serializers.ModelSerializer):
    """Serializer for Benefit objects"""

    # user = serializers.StringRelatedField(read_only=True)
    # company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Benefit
        fields = ['title', 'blurb', 'icon_url']
        # fields = "__all__"


class CompanyChatbotSerializer(serializers.ModelSerializer):
    """Serializer for CompanyChatbot objects"""

    # user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CompanyChatbot
        fields = [
            'company',
            'career_site_url',
            'privacy_notice_url',
            'benefits_url',
            'benefits_message',
            'next_steps',
            'company_video_url',
            'talent_email'
        ]
        # fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location objects"""

    # user = serializers.StringRelatedField(read_only=True)
    # company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Location
        # fields = "__all__"
        fields = ['street_address', 'city', 'country']


class JobMapSerializer(serializers.ModelSerializer):
    """Serializer for JobMap objects"""

    # user = serializers.StringRelatedField(read_only=True)
    # company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = JobMap
        # fields = "__all__"
        fields = ['specialism', 'category_one']


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job objects"""

    # user = serializers.StringRelatedField(read_only=True)
    # company = serializers.StringRelatedField(read_only=True)
    location = LocationSerializer(read_only=True)
    specialism = JobMapSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'location',
            'specialism',
            'title',
            'role_type',
            'description_url',
            'apply_url',
            'video_url',
            'intro'
        ]
        # fields = "__all__"
