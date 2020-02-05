from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_api_key.models import APIKey

from core.models import Company, Question

from chatbot.serializers import QuestionSerializer


def sample_question(user, company, **params):
    """Create and return sample question"""

    defaults = {
        'topic': 'prepareApplication',
        'question': 'Preparing your CV',
        'answer': "We want to hear about what you've achieved, your strengths\
                  and skills.\n\nWe also want to know how you can apply them \
                  to the job you're applying for.",
        'active_question': True
    }
    defaults.update(params)

    return Question.objects.create(
        user=user,
        company=company,
        **defaults
    )


def get_url(company):
    """Returns the get url to call for the question"""

    keywords = {'company_pk': company.id}
    return reverse('chatbot:question-list', kwargs=keywords)


class PublicQuestionApiTests(TestCase):
    """Test the publicly available question API"""

    def setUp(self):
        self.client = APIClient()

    def test_permission_required(self):
        """Test that permission is required for accessing question"""
        company = Company.objects.create(company_name='PiedPiper')
        keywords = {'company_pk': company.id}
        QUESTION_URL = reverse('chatbot:question-list', kwargs=keywords)

        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateQuestionApiTests(TestCase):
    """Test the private question API"""

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

    def test_retrieving_question_list(self):
        """Test retrieving questions for a company"""

        sample_question(self.user, self.company)

        sample_question(self.user, self.company, topic='flexibleWorking')

        QUESTION_URL = get_url(self.company)

        res = self.client.get(QUESTION_URL)

        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_questions_limited_by_company(self):
        """Test that questions for the authenticated company is returned"""
        company2 = Company.objects.create(company_name='Hooli')

        sample_question(self.user, company2)

        data = sample_question(self.user, self.company)

        QUESTION_URL = get_url(self.company)

        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['topic'],
            data.topic
        )

    def test_active_questions_returned(self):
        """Test that only active questions are returned"""

        sample_question(self.user, self.company, active_question=False)

        data = sample_question(self.user, self.company)

        QUESTION_URL = get_url(self.company)

        res = self.client.get(QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(
            res.data[0]['topic'],
            data.topic
        )
