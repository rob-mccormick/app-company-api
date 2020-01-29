from rest_framework import serializers

from core.models import CompanyChatbot


class CompanyChatbotSerializer(serializers.ModelSerializer):
    """Serializer for CompanyChatbot objects"""

    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CompanyChatbot
        fields = "__all__"
