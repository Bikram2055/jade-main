from django.db import models
from phone_field import PhoneField

from src.users.models import TimeStampAbstractModel, User


# Create your models here.
class Employer(TimeStampAbstractModel):

    description = models.CharField(max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self) -> str:
        return self.user.username
