from django.test import TestCase
# from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import CbBrowsingData, Company


def sample_browsing_data(company, **params):
    """Create and return sample browsing data"""
    defaults = {
        'chatbot_user_id': 'abc123-3',
        'date_time': '2019-12-03T12:34:56Z',
        'is_browsing': 'true'
    }
    defaults.update(params)

    return CbBrowsingData.objects.create(company=company, **defaults)


class PublicCbQnsDataApiTests(TestCase):
    """Test the publicly available cbbrowsingdata API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing cbqnsdata"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTBROWSINGDATA_URL = reverse('cbdata:cbbrowsingdata-create',
                                       kwargs=keywords)
        res = self.client.get(POSTBROWSINGDATA_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCbQnsDataApiTests(TestCase):
    """Test the private cbbrowsingdata API"""

    def setUp(self):
        api_key, key = APIKey.objects.create_key(name="tests")

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    def test_post_browsing_data_successful(self):
        """Test posting new browsing data from the chatbot"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTBROWSINGDATA_URL = reverse('cbdata:cbbrowsingdata-create',
                                       kwargs=keywords)
        payload = {
            'chatbot_user_id': 'abc123-3',
            'date_time': '2019-12-03T12:34:56Z',
            'is_browsing': True
        }

        res = self.client.post(POSTBROWSINGDATA_URL, payload)

        exists = CbBrowsingData.objects.filter(
            chatbot_user_id=payload['chatbot_user_id']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_browsingdata_invalid(self):
        """Test posting new browsing data with invalid payload"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTBROWSINGDATA_URL = reverse('cbdata:cbqnsdata-create',
                                       kwargs=keywords)
        payload = {
            'chatbot_user_id': 'abc123-3',
            'date_time': ''
        }

        res = self.client.post(POSTBROWSINGDATA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    """
    - Authorised user cannot post
    - Admin user cannot post
    - Authorized API Key can post
    - Authorized API Key cannot post invalid data
    - API Key cannot post for another company
    """
