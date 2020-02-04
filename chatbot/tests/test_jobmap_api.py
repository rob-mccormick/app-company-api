from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Company, JobMap

from chatbot.serializers import JobMapSerializer


class PublicJobMapApiTests(TestCase):
    """Test the publicly available jobmap API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing jobmap api"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        JOBMAP_URL = reverse('chatbot:jobmap-list', kwargs=keywords)

        res = self.client.get(JOBMAP_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateJobMapApiTests(TestCase):
    """Test the private jobmap API"""

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

    def test_retrieving_jobmap_list(self):
        """Test retrieving the company jobmap"""

        JobMap.objects.create(
            user=self.user,
            company=self.company,
            specialism='Designer',
            category_one='Building the product'
        )

        JobMap.objects.create(
            user=self.user,
            company=self.company,
            specialism='Sales',
            category_one='Growing the business'
        )

        keywords = {'company_pk': self.company.id}
        JOBMAP_URL = reverse('chatbot:jobmap-list', kwargs=keywords)

        res = self.client.get(JOBMAP_URL)

        jobmaps = JobMap.objects.all()
        serializer = JobMapSerializer(jobmaps, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_jobmap_limited_by_company(self):
        """Test that jobmap info for the authenticated company is returned"""

        company2 = Company.objects.create(company_name='Hooli')
        JobMap.objects.create(
            user=self.user,
            company=company2,
            specialism='Designer',
            category_one='Building the product'
        )

        data = JobMap.objects.create(
            user=self.user,
            company=self.company,
            specialism='Sales',
            category_one='Growing the business'
        )

        keywords = {'company_pk': self.company.id}
        JOBMAP_URL = reverse('chatbot:jobmap-list', kwargs=keywords)

        res = self.client.get(JOBMAP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['company'],
            data.company.company_name
        )
