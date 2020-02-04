from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Company, CompanyChatbot

from chatbot.serializers import CompanyChatbotSerializer


def sample_company_chatbot_data(user, company, company_name, **params):
    """Create and return sample company chatbot info"""

    defaults = {
        'career_site_url': f'https://www.{ company_name }.com/careers',
        'privacy_notice_url': f'https://www.{ company_name }.com/privacy',
        'next_steps': 'We will get back to you in 2 working days.',
        'talent_email': f'talent@{ company_name }.com'
    }
    defaults.update(params)

    return CompanyChatbot.objects.create(
        user=user,
        company=company,
        **defaults
    )


class PublicCompanyChatbotApiTests(TestCase):
    """Test the publicly available companychatbot API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing companychatbot"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        COMPANYCHATBOT_URL = reverse('chatbot:companychatbot-list',
                                     kwargs=keywords)

        res = self.client.get(COMPANYCHATBOT_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCompanyChatbotApiTests(TestCase):
    """Test the private companychatbot API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.company = Company.objects.create(company_name='PiedPiper')

        api_key, key = APIKey.objects.create_key(
            name="PiedPiper API Key",
        )

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    def test_retrieving_company_chatbot_list(self):
        """Test retrieving the info for a company chatbot"""

        sample_company_chatbot_data(
            user=self.user,
            company=self.company,
            company_name='piedpiper'
        )

        keywords = {'company_pk': self.company.id}
        COMPANYCHATBOT_URL = reverse('chatbot:companychatbot-list',
                                     kwargs=keywords)

        res = self.client.get(COMPANYCHATBOT_URL)

        companychatbots = CompanyChatbot.objects.all()
        serializer = CompanyChatbotSerializer(companychatbots, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_companychatbot_limited_by_company(self):
        """Test that chatbot info for the authenticated company is returned"""

        company2 = Company.objects.create(company_name='Hooli')
        sample_company_chatbot_data(
            user=self.user,
            company=company2,
            company_name='hooli'
        )

        data = sample_company_chatbot_data(
            user=self.user,
            company=self.company,
            company_name='piedpiper'
        )

        keywords = {'company_pk': self.company.id}
        COMPANYCHATBOT_URL = reverse('chatbot:companychatbot-list',
                                     kwargs=keywords)

        res = self.client.get(COMPANYCHATBOT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['company'],
            data.company.company_name
        )
