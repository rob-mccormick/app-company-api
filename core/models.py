import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Company(models.Model):
    """Company object"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name


class CbJobsData(models.Model):
    """Jobs data from chatbot conversations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
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


class RoleType(models.Model):
    """Role types for the company"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role_type = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.role_type }'


class Job(models.Model):
    """Job objects"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    specialism = models.ManyToManyField(JobMap)
    title = models.CharField(max_length=100)
    role_type = models.ForeignKey(RoleType, on_delete=models.CASCADE)
    description_url = models.CharField(max_length=255)
    apply_url = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, blank=True)
    intro = models.CharField(max_length=255, blank=True)
    active_job = models.BooleanField(default=False)
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


class CompanyChatbot(models.Model):
    """Company chatbot info object"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    career_site_url = models.CharField(max_length=255)
    privacy_notice_url = models.CharField(max_length=255)
    benefits_url = models.CharField(max_length=255, blank=True)
    benefits_message = models.CharField(max_length=255, blank=True)
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


class QuestionTopic(models.Model):
    """Question topics for the company"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    index = models.CharField(max_length=60)
    string = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.index }'


class Question(models.Model):
    """Questions provided by the company"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    topic = models.ForeignKey(QuestionTopic, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.TextField()
    active_question = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.company.company_name } - { self.question }'

    def serialize_hook(self, hook):
        """Create a skinny payload to notify chatbot of change"""
        return {
            'hook': hook.dict(),
            'data': {
                'change': True
            }
        }
