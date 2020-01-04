from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


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
