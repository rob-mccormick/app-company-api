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

    def test_cbbrowsingdata_str(self):
        """Test the cbbrowsingdata string representation"""
        browsingdata = models.CbBrowsingData.objects.create(
            company=models.Company.objects.create(company_name='PiedPiper'),
            chatbot_user_id='abc123',
            date_time='2020-01-04T09:43:56Z',
            is_browsing=True,
            why_on_site=''
        )

        self.assertEqual(
            str(browsingdata),
            f'{browsingdata.company.company_name} - {browsingdata.date_time}'
        )

    def test_locations_str(self):
        """Test the location string representation"""
        test_user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Testpass123'
        )
        location = models.Location.objects.create(
            user=test_user,
            company=models.Company.objects.create(company_name='PiedPiper'),
            street_address='123 Mare Street',
            city='London',
            country='United Kingdom',
            post_code='E8 3AB'
        )

        self.assertEqual(
            str(location),
            f'{location.company.company_name} - {location.city}'
        )

    def test_jobs_str(self):
        """Test the jobs string representation"""
        test_company = models.Company.objects.create(company_name='Hooli')
        test_user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Testpass123'
        )
        job = models.Job.objects.create(
            user=test_user,
            company=test_company,
            title='Web Developer',
            location=models.Location.objects.create(
                user=test_user,
                company=test_company,
                street_address='123 Mare Street',
                city='London',
                country='United Kingdom',
                post_code='E8 3AB'
            ),
            role_type='Individual Contributor',
            description_url='https://www.idealrole.com/apply/123',
            apply_url='https://www.idealrole.com/apply/123/apply',
            active_job=True
        )

        self.assertEqual(
            str(job),
            f'{job.company.company_name} - {job.title}'
        )

    def test_company_chatbot_str(self):
        """Test the company chatbot string representation"""
        test_company = models.Company.objects.create(company_name='Hooli')
        test_user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Testpass123'
        )

        company_chatbot = models.CompanyChatbot.objects.create(
            user=test_user,
            company=test_company,
            career_site_url='https://www.company.com/careers',
            privacy_notice_url='https://www.company.com/privacy',
            next_steps='get back to you in 3 days.',
            talent_email='careers@company.com'
        )

        self.assertEqual(
            str(company_chatbot),
            f'{company_chatbot.company.company_name} Chatbot Info'
        )

    def test_company_apikey_str(self):
        """Test the company apikey string representation"""
        test_company = models.Company.objects.create(company_name='Hooli')
        test_apikey = models.CompanyAPIKey.objects.create(
            name='Hooli API Key',
            company=test_company
        )

        self.assertEqual(
            str(test_apikey),
            f'{test_apikey.company.company_name} API Key'
        )

    def test_jobmap_str(self):
        """Test the jobmapping string representation"""
        test_company = models.Company.objects.create(company_name='Hooli')
        test_user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Testpass123'
        )
        test_jobmap = models.JobMap.objects.create(
            user=test_user,
            company=test_company,
            specialism='Design',
            category_one='Building the product'
        )

        self.assertEqual(
            str(test_jobmap),
            f'{test_jobmap.company.company_name} - {test_jobmap.specialism}'
        )

    def test_benefit_str(self):
        """Test the benefit string representation"""
        test_company = models.Company.objects.create(company_name='Hooli')
        test_user = get_user_model().objects.create_user(
            email='test@email.com',
            password='Testpass123'
        )
        test_benefit = models.Benefit.objects.create(
            user=test_user,
            company=test_company,
            title='Paid parental leave',
            active_benefit=True
        )

        self.assertEqual(
            str(test_benefit),
            f'{test_benefit.company.company_name} - {test_benefit.title}'
        )
