from rest_framework import serializers

from core.models import Benefit, CompanyChatbot, Job, JobMap, Location, \
                        Question, QuestionTopic


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


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location objects"""

    class Meta:
        model = Location
        fields = ['street_address', 'city', 'country']


class JobMapSerializer(serializers.ModelSerializer):
    """Serializer for JobMap objects"""

    class Meta:
        model = JobMap
        fields = ['specialism', 'category_one']


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job objects"""

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


class QuestionTopicSerializer(serializers.ModelSerializer):
    """Serializer for QuestionTopic objects"""

    class Meta:
        model = QuestionTopic
        fields = ['index', 'string']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question objects"""

    topic = QuestionTopicSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['topic', 'question', 'answer']
