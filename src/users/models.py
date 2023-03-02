import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.signals import saved_file
from rest_framework_simplejwt.tokens import RefreshToken

from src.common.helpers import build_absolute_uri
from src.notifications.services import ACTIVITY_USER_RESETS_PASS, notify


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    """
    reset_password_path = reverse('password_reset:reset-password-confirm')
    context = {
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': build_absolute_uri(f'{reset_password_path}?token={reset_password_token.key}'),
    }

    notify(ACTIVITY_USER_RESETS_PASS, context=context, email_to=[reset_password_token.user.email])


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Email address",
        max_length=255,
        unique=True,
    )
    profile_picture = ThumbnailerImageField('ProfilePicture', upload_to='profile_pictures/', blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __str__(self):
        return self.username


saved_file.connect(generate_aliases_global)


class TimeStampAbstractModel(models.Model):
    """Inherit from this class to add timestamp fields in the model class"""

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    """DateField: date on which the instance is created."""
    updated_at = models.DateTimeField(auto_now=True, null=True)
    """DateField: date on which the instance is updated."""

    class Meta:
        abstract = True


class Address(TimeStampAbstractModel):
    '''This class to add user address'''

    country = models.CharField(max_length=30)
    '''CharField: country of user'''
    city = models.CharField(max_length=30)
    '''CharField: city of user'''
    street = models.CharField(max_length=30)
    '''CharField: street of user'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    '''OneToOneField: one user linked with one address'''
