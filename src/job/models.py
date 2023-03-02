from django.db import models

from src.employer.models import Employer
from src.job_seeker.models import Job_Seeker
from src.users.models import TimeStampAbstractModel


# Create your models here.
class Category(TimeStampAbstractModel):
    '''This class for add category for jobs'''

    category = models.CharField(max_length=30)


class Required_Skill(TimeStampAbstractModel):
    '''This class is for skills set required to fullfill specific project'''

    skill = models.CharField(max_length=30)
    '''CharField: for skill required for project'''

    def __str__(self) -> str:
        return self.skill


class Job(TimeStampAbstractModel):
    '''This class for add jobs by employer'''

    name = models.CharField(max_length=30)
    '''CharField: for name of project'''
    description = models.CharField(max_length=250)
    '''CharField: for description of project'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    '''ForeginKey: for category of the project'''
    budget = models.FloatField()
    '''FloatField: for define budget of project'''
    duration = models.DateField(null=True)
    '''DateField: for last date of project'''
    requirement = models.FileField()
    '''FileField: for file related to project'''
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    '''ForeginKey: for which employer add the project'''
    is_draft = models.BooleanField(default=False)
    '''BooleanField: for status of project to save as draft'''
    skill = models.ManyToManyField(Required_Skill)

    def __str__(self) -> str:
        return self.name


class Project(TimeStampAbstractModel):
    '''This class for Project status'''

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_project')
    '''ForeignKey: for specific project status'''
    job_seeker = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    '''ForeignKey: for specific employee who is doing such project'''
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    '''ForeignKey: for specific employer who add such project'''
    is_active = models.BooleanField(default=True)
    '''BooleanField: for status of project is active or not'''
    is_finished = models.BooleanField(default=False)
    '''BooleanField: for status of project is finished or not'''


class Bid(TimeStampAbstractModel):
    '''This class is for record of job_seekers who wants to do specific job'''

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    '''ForeignKey: for specific project'''
    proposal = models.CharField(max_length=150)
    '''CharField: for proposal given by job_seeker to project'''
    amount = models.FloatField()
    '''FloatField: for job_seeker biding amount'''
    job_seeker = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    '''ForeignKey: for specify job_seeker'''
    require_days = models.IntegerField()
    '''IntegerField: for number of days to complete the project assigned by job seeker'''
    milestone = models.CharField(max_length=300)
    '''CharField: for set milestone of project'''
    is_shortlisted = models.BooleanField(default=False)
    '''BooleanField: for status of shortlisted job seeker by employer'''


class Rating(TimeStampAbstractModel):
    """This is a Django model definition for a Rating model.
    The Rating model inherits from a custom abstract model named TimeStampAbstractModel,
    which presumably adds timestamp fields for created and modified dates to the Rating model.
    """

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    '''employer: A foreign key to the Employer model, with a CASCADE on delete behavior.
    This field represents the employer who submitted the rating.'''
    job_seeker = models.ForeignKey(Job_Seeker, on_delete=models.CASCADE)
    '''job_seeker: A foreign key to the Job_Seeker model, with a CASCADE on delete behavior.
    This field represents the job seeker who was rated.'''
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    '''job: A foreign key to the Job model, with a CASCADE on delete behavior.
    This field represents the job that the rating is associated with.'''
    rating = models.FloatField()
    '''rating: A floating-point field representing the rating score given by the employer to the job seeker.'''
    feedback = models.CharField(max_length=250, null=True, blank=True)
    '''feedback: A string field with a maximum length of 250 characters, representing any feedback or comments the
    employer may have provided along with the rating. This field is optional, as it allows null and blank values.'''
