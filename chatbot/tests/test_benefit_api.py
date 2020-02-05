from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Benefit, Company

from chatbot.serializers import BenefitSerializer


class PublicBenefitApiTests(TestCase):
    """Test the publicly available benefit API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing the benefit API"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        BENEFIT_URL = reverse('chatbot:benefit-list', kwargs=keywords)

        res = self.client.get(BENEFIT_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateBenefitApiTests(TestCase):
    """Test the private benefit API"""

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

    def test_retrieving_benefit_list(self):
        """Test retrieving the company benefits"""

        Benefit.objects.create(
            user=self.user,
            company=self.company,
            title='Parental Leave',
            active_benefit=True
        )

        Benefit.objects.create(
            user=self.user,
            company=self.company,
            title='Learning and Development',
            icon_url='https://www.piedpiper/careers/#learning',
            active_benefit=True
        )

        keywords = {'company_pk': self.company.id}
        BENEFIT_URL = reverse('chatbot:benefit-list', kwargs=keywords)

        res = self.client.get(BENEFIT_URL)

        benefits = Benefit.objects.all()
        serializer = BenefitSerializer(benefits, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_benefits_limited_by_company(self):
        """Test that benefit info for the authenticated company is returned"""

        company2 = Company.objects.create(company_name='Hooli')
        Benefit.objects.create(
            user=self.user,
            company=company2,
            title='Yoga classes and retreats',
            active_benefit=True
        )

        data = Benefit.objects.create(
            user=self.user,
            company=self.company,
            title='Learning and Development',
            icon_url='https://www.piedpiper/careers/#learning',
            active_benefit=True
        )

        keywords = {'company_pk': self.company.id}
        BENEFIT_URL = reverse('chatbot:benefit-list', kwargs=keywords)

        res = self.client.get(BENEFIT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['title'],
            data.title
        )

    def test_active_benefits_returned(self):
        """Test that only active benefits are returned"""

        Benefit.objects.create(
            user=self.user,
            company=self.company,
            title='Yoga classes and retreats',
            active_benefit=False
        )

        data = Benefit.objects.create(
            user=self.user,
            company=self.company,
            title='Learning and Development',
            icon_url='https://www.piedpiper/careers/#learning',
            active_benefit=True
        )

        keywords = {'company_pk': self.company.id}
        BENEFIT_URL = reverse('chatbot:benefit-list', kwargs=keywords)

        res = self.client.get(BENEFIT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['title'],
            data.title
        )
