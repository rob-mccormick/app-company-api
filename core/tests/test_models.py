from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@email.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@email.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_company_str(self):
        """Test the company string representation"""
        company = models.Company.objects.create(
            company_name='PiedPiper'
        )

        self.assertEqual(str(company), company.company_name)

    def test_cbjobsdata_str(self):
        """Test the cbjobsdata string representation"""
        jobsdata = models.CbJobsData.objects.create(
            company=models.Company.objects.create(company_name='PiedPiper'),
            chatbot_user_id='abc123',
            date_time='2019-12-03T12:34:56Z',
            specialism_search='Engineering',
            location_search='London',
            role_type_search='Leader'
        )

        self.assertEqual(
            str(jobsdata),
            f'{jobsdata.company.company_name} - {jobsdata.date_time}'
        )

    def test_cbqnsdata_str(self):
        """Test the cbquesdata string representation"""
        qnsdata = models.CbQnsData.objects.create(
            company=models.Company.objects.create(company_name='PiedPiper'),
            chatbot_user_id='abc123',
            date_time='2020-01-04T09:43:56Z',
            has_question=True,
            search_question='Flexible working options',
            question_helpful=False,
            wants_reply=False
        )

        self.assertEqual(
            str(qnsdata),
            f'{qnsdata.company.company_name} - {qnsdata.date_time}'
        )
