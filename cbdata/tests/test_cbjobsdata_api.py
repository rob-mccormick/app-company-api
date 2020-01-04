from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient, force_authenticate
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import CbJobsData, Company


def sample_jobs_data(company, **params):
    """Create and return sample job data"""
    defaults = {
        'chatbot_user_id': 'abc123-3',
        'date_time': '2019-12-03T12:34:56Z',
        'specialism_search': 'Product',
        'location_search': 'London',
        'role_type_search': 'Individual contributor'
    }
    defaults.update(params)

    return CbJobsData.objects.create(company=company, **defaults)


class PublicCbJobsDataApiTests(TestCase):
    """Test the publicly available cbjobsdata API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for accessing cbjobsdata"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTJOBSDATA_URL = reverse('cbdata:cbjobsdata-create',
                                   kwargs=keywords)
        res = self.client.get(POSTJOBSDATA_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateCbJobsDataApiTests(TestCase):
    """Test the private cbjobsdata API"""

    def setUp(self):
        api_key, key = APIKey.objects.create_key(name="tests")

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)

    def test_post_job_data_successful(self):
        """Test posting new job data from the chatbot"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTJOBSDATA_URL = reverse('cbdata:cbjobsdata-create',
                                   kwargs=keywords)
        payload = {
            'chatbot_user_id': 'abc123-3',
            'date_time': '2019-12-03T12:34:56Z',
            'specialism_search': 'Product',
            'location_search': 'London',
            'role_type_search': 'Individual contributor',
            'found_job': 'true'
        }

        res = self.client.post(POSTJOBSDATA_URL, payload)

        exists = CbJobsData.objects.filter(
            chatbot_user_id=payload['chatbot_user_id']
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_jobsdata_invalid(self):
        """Test posting new jobs data with invalid payload"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        POSTJOBSDATA_URL = reverse('cbdata:cbjobsdata-create',
                                   kwargs=keywords)
        payload = {
            'chatbot_user_id': 'abc123-3',
            'date_time': '2019-12-03T12:34:56Z',
            'specialism_search': '',
            'location_search': '',
            'role_type_search': 'Individual contributor'
        }
        res = self.client.post(POSTJOBSDATA_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    """
    - Authorised user cannot post
    - Admin user cannot post
    - Authorized API Key can post
    - Authorized API Key cannot post invalid data
    - API Key cannot post for another company
    """
