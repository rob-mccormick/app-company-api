import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from rest_framework_api_key.models import AbstractAPIKey


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("We need an email address - try again")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(PermissionsMixin, AbstractBaseUser):
    """Custom model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Company(models.Model):
    """Company object"""
    company_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name


class CbJobsData(models.Model):
    """Jobs data from chatbot conversations"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    chatbot_user_id = models.CharField(max_length=60)
    date_time = models.DateTimeField()
    specialism_search = models.CharField(max_length=100)
    location_search = models.CharField(max_length=60)
    role_type_search = models.CharField(max_length=100)
    found_job = models.NullBooleanField()
    saw_benefits = models.NullBooleanField()
    saw_company_video = models.NullBooleanField()
    saw_job_video = models.NullBooleanField()
    add_to_pipeline = models.NullBooleanField()
    joined_pipeline = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Chatbot job data"

    def __str__(self):
        return f'{ self.company.company_name } - { self.date_time }'


class CbQnsData(models.Model):
    """Questions data from chatbot conversations"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    chatbot_user_id = models.CharField(max_length=60)
    date_time = models.DateTimeField()
    has_question = models.BooleanField(default=False)
    search_question = models.CharField(max_length=100, blank=True)
    question_helpful = models.NullBooleanField()
    wants_reply = models.NullBooleanField()
    question_left = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Chatbot question data"

    def __str__(self):
        return f'{ self.company.company_name } - { self.date_time }'


class CbBrowsingData(models.Model):
    """Browsing data from chatbot conversations"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    chatbot_user_id = models.CharField(max_length=60)
    date_time = models.DateTimeField()
    is_browsing = models.BooleanField(default=False)
    why_on_site = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Chatbot browsing data"

    def __str__(self):
        return f'{ self.company.company_name } - { self.date_time }'


class Location(models.Model):
    """Office locations for each company"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    post_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.city }'

    def serialize_hook(self, hook):
        """Create a skinny payload to notify chatbot of change"""
        return {
            'hook': hook.dict(),
            'data': {
                'change': True
            }
        }


class Job(models.Model):
    """Job objects"""
    # user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    specialism = models.CharField(max_length=100)
    role_type = models.CharField(max_length=100)
    description_url = models.CharField(max_length=255)
    apply_url = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, blank=True)
    intro = models.CharField(max_length=255, blank=True)
    active_job = models.BooleanField(default=False)

    def __str__(self):
        return f'{ self.company.company_name } - { self.title }'


class CompanyChatbot(models.Model):
    """Company chatbot info object"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    career_site_url = models.CharField(max_length=255)
    benefits_url = models.CharField(max_length=255, blank=True)
    benefits_message = models.CharField(max_length=255, blank=True)
    privacy_notice_url = models.CharField(max_length=255)
    next_steps = models.CharField(max_length=255)
    company_video_url = models.CharField(max_length=255, blank=True)
    talent_email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } Chatbot Info'

    def serialize_hook(self, hook):
        """Create a skinny payload to notify chatbot of change"""
        return {
            'hook': hook.dict(),
            'data': {
                'change': True
            }
        }


class CompanyAPIKey(AbstractAPIKey):
    """Extension of APIKey specific to the company"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = 'Company API Key'
        verbose_name_plural = 'Companies API Keys'

    def __str__(self):
        return f'{ self.company.company_name } API Key'


class JobMap(models.Model):
    """Mapping jobs to categories for job search"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    specialism = models.CharField(max_length=60)
    category_one = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.specialism }'

    def serialize_hook(self, hook):
        """Create a skinny payload to notify chatbot of change"""
        return {
            'hook': hook.dict(),
            'data': {
                'change': True
            }
        }


class Benefit(models.Model):
    """Benefits provided by the company"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    blurb = models.CharField(max_length=255, blank=True)
    icon_url = models.CharField(max_length=255, blank=True)
    active_benefit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.title }'

    def serialize_hook(self, hook):
        """Create a skinny payload to notify chatbot of change"""
        return {
            'hook': hook.dict(),
            'data': {
                'change': True
            }
        }
