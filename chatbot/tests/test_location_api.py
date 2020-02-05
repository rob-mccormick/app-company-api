from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Company, Location

from chatbot.serializers import LocationSerializer


def sample_location(user, company, city, **params):
    """Create and return sample location"""

    defaults = {
        'street_address': '143 Main Street',
        'country': 'United States',
        'post_code': '123-4444'
    }
    defaults.update(params)

    return Location.objects.create(
        user=user,
        company=company,
        city=city,
        **defaults
    )


class PublicLocationApiTests(TestCase):
    """Test the publicly available location API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing location"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        LOCATION_URL = reverse('chatbot:location-list', kwargs=keywords)

        res = self.client.get(LOCATION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateLocationApiTests(TestCase):
    """Test the private location API"""

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

    def test_retrieving_location_list(self):
        """Test retrieving locations for a company"""

        sample_location(self.user, self.company, 'Silicon Valley')

        sample_location(self.user, self.company, 'Oakland')

        keywords = {'company_pk': self.company.id}
        LOCATION_URL = reverse('chatbot:location-list', kwargs=keywords)

        res = self.client.get(LOCATION_URL)

        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_locations_limited_by_company(self):
        """Test that locations for the authenticated company is returned"""
        company2 = Company.objects.create(company_name='Hooli')

        sample_location(self.user, company2, 'Silicon Valley')

        data = sample_location(self.user, self.company, 'Silicon Valley')

        keywords = {'company_pk': self.company.id}
        LOCATION_URL = reverse('chatbot:location-list', kwargs=keywords)

        res = self.client.get(LOCATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['city'],
            data.city
        )
