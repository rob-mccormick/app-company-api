from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Company, Job, Location

from chatbot.serializers import JobSerializer


def sample_location(user, company, **params):
    """Create and return sample location"""

    defaults = {
        'city': 'Silicon Valley',
        'street_address': '143 Main Street',
        'country': 'United States',
        'post_code': '123-4444'
    }
    defaults.update(params)

    return Location.objects.create(
        user=user,
        company=company,
        **defaults
    )


def sample_job(user, company, title, **params):
    """Create and return a sample job"""

    location = sample_location(user=user, company=company)

    defaults = {
        'location': location,
        'role_type': 3,
        'description_url': 'http://www.piedpiper.com/job/23',
        'apply_url': 'http://www.piedpiper.com/job/23/apply',
        'active_job': True
    }
    defaults.update(params)

    return Job.objects.create(
        user=user,
        company=company,
        title=title,
        **defaults
    )


class PublicJobApiTests(TestCase):
    """Test the publicly available job API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing job API"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        JOB_URL = reverse('chatbot:job-list', kwargs=keywords)

        res = self.client.get(JOB_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateJobApiTests(TestCase):
    """Test the private job API"""

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

    def test_retrieving_job_list(self):
        """Test retrieving the company jobs"""

        sample_job(
            user=self.user,
            company=self.company,
            title='Front End Engineer'
        )

        sample_job(
            user=self.user,
            company=self.company,
            title='Customer Success Manager'
        )

        keywords = {'company_pk': self.company.id}
        JOB_URL = reverse('chatbot:job-list', kwargs=keywords)

        res = self.client.get(JOB_URL)

        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_jobs_limited_by_company(self):
        """Test that only jobs for the authenticated company is returned"""

        company2 = Company.objects.create(company_name='Hooli')

        sample_job(
            user=self.user,
            company=company2,
            title='Front End Engineer'
        )

        data = sample_job(
            user=self.user,
            company=self.company,
            title='Customer Success Manager'
        )

        keywords = {'company_pk': self.company.id}
        JOB_URL = reverse('chatbot:job-list', kwargs=keywords)

        res = self.client.get(JOB_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['title'],
            data.title
        )

    def test_active_jobs_returned(self):
        """Test that only active jobs are returned"""

        sample_job(
            user=self.user,
            company=self.company,
            title='Front End Engineer',
            active_job=False
        )

        data = sample_job(
            user=self.user,
            company=self.company,
            title='Customer Success Manager'
        )

        keywords = {'company_pk': self.company.id}
        JOB_URL = reverse('chatbot:job-list', kwargs=keywords)

        res = self.client.get(JOB_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['title'],
            data.title
        )
