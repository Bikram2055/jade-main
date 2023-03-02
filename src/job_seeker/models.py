from django.db import models
from phone_field import PhoneField

from src.users.models import TimeStampAbstractModel, User


# Create your models here.
class Skill(TimeStampAbstractModel):
    """This is a Django model class for the Skill model. It is a subclass of TimeStampAbstractModel,
     which is likely a custom abstract base model that adds timestamp fields (e.g. created_at, updated_at)
      to the model.

    The Skill model has one field, skill, which is a character field with a maximum length of 30 characters.

    The __str__ method returns a string representation of the Skill instance, which will be used as the string
     representation of the object in the Django administration interface and in other parts of the application
      where the object needs to be represented as a string. In this case, it returns the value of the skill field.
    """

    skill = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.skill


class Job_Seeker(TimeStampAbstractModel):
    """This model represents job seekers, and the fields correspond to information that is typically
    associated with job seekers, such as their education, experience, phone number, and skills.
    """

    education = models.CharField(max_length=250)
    '''a character field with a maximum length of 250 characters.'''
    experience = models.FloatField()
    '''a float field that stores a numerical value.'''
    phone = PhoneField(blank=True)
    '''a PhoneField field, which is likely a custom field type for storing phone numbers.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ''' a one-to-one field that links the Job_Seeker model to the Django User model. The on_delete
    argument specifies the behavior when the referenced User instance is deleted. In this case,
    it is set to models.CASCADE, meaning that if the User instance is deleted, the related Job_Seeker
    instance will also be deleted.'''
    skill = models.ManyToManyField(Skill)
    '''a many-to-many field that links the Job_Seeker model to the Skill model. This allows a Job_Seeker
    instance to have multiple Skill instances associated with it.'''

    def __str__(self) -> str:
        return self.user.username
