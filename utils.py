from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.conf import settings
import hashlib, logging


"""
Custom user model manager where email is the unique identifiers
for authentication instead of username.
"""
class UserModelManager(BaseUserManager):
    # Create and save a user with the given email and password.
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("User must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create and save a SuperUser with the given email and password.
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    

"""
Custom JWT Authentication where access token is checked for blackilisting
before authentication.
"""
class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        # Validate the token using the default mechanism
        validated_token = super().get_validated_token(raw_token)
        
        # Create a cache key using the token's string representation
        cache_key = self.get_cache_key(str(validated_token))
        
        # Check if the token is blacklisted in the cache
        if cache.get(cache_key) == 'blacklisted':
            raise AuthenticationFailed("This token has been blacklisted.")

        return validated_token

    def get_cache_key(self, token_str):
        """
        Generates a cache key based on the token string by hashing the token.
        You can also include additional logic to create a unique key.
        """
        return hashlib.sha256(token_str.encode()).hexdigest()
    

# Get the email and general error logger
email_logger = logging.getLogger('email_logger')
general_logger = logging.getLogger('general_logger')


# Asynchronous email sending
def send_async_email(email_subject, email_body, email_recipient, email_headers=None):
    try:
        email_sender = settings.DEFAULT_FROM_EMAIL
        email = EmailMultiAlternatives(email_subject, email_body, email_sender, email_recipient, headers=email_headers)
        email.send()
    except Exception as e:
        email_logger.error(f"Error sending email: {e}")
