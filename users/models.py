from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django_rest_passwordreset.models import ResetPasswordToken
from uuid import uuid4
from datetime import timedelta
from .utils import UserModelManager
import random


# Create your models here.
class UserModel(AbstractUser):
    """
    This model will serve as the default authentication model via AUTH_USER_MODEL in settings.py
    """
    username = None
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = UserModelManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-date_joined']


class CustomPasswordResetToken(ResetPasswordToken):
    """
    Proxy model to override the behavior of ResetPasswordToken.
    """
    class Meta:
        proxy = True

    @staticmethod
    def generate_key():
        """
        Override the generate_key method to generate a 6-digit OTP.
        """
        return f"{random.randint(100000, 999999)}"

    def is_expired(self):
        """
        Check if the OTP has expired.
        """
        expiration_time = timedelta(minutes=10) #Set expiration duration to 10 minutes
        return now() > self.created_at + expiration_time
    