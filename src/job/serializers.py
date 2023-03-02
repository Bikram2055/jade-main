from rest_framework import serializers

from src.employer.serializers import EmployernameSerializer
from src.job.models import Bid, Category, Job, Project, Rating, Required_Skill


class RequireskillSerializer(serializers.ModelSerializer):
    """This is a Django REST Framework serializer for the Required_Skill model. The RequireskillSerializer
    has a nested Meta class that defines the model to be serialized and the fields to be included in the
    serialized output. The RequireskillSerializer includes a single field:

    skill: This is a CharField representing the required skill for a job.
    The RequireskillSerializer is used to serialize and deserialize data between Python objects
    and JSON, so it can be used to communicate with an API that returns or accepts data in JSON format.
    When the serializer is used to serialize an instance of the model, it will convert the model data into
    a JSON object that has the same structure as the serializer. Conversely, when the serializer is used to
    deserialize a JSON object, it will convert the JSON data into a Python object that has the same structure
    as the serializer.
    """

    class Meta:
        model = Required_Skill
        fields = ['skill']


class CategorySerializer(serializers.ModelSerializer):
    """This is a Django REST Framework serializer for the Category model. The CategorySerializer
    has a nested Meta class that defines the model to be serialized and the fields to be included
    in the serialized output. The CategorySerializer includes a single field:

    category: This is a CharField representing the name of the category.
    """

    class Meta:
        model = Category
        fields = ['category']


class JobSerializer(serializers.ModelSerializer):
    """This is a Django REST Framework serializer for the Job model, with several nested serializers
    that handle related models. The JobSerializer has a nested Meta class that defines the model to be
    serialized and the fields to be included in the serialized output. The JobSerializer includes the
    following fields:

    name: This is a CharField representing the name of the job.

    description: This is a CharField representing the description of the job.

    category_name: This is a nested serializer CategorySerializer which serializes the category model
    instance associated with the job.

    budget: This is a FloatField representing the budget for the job.

    duration: This is a CharField representing the duration of the job.

    requirement: This is a CharField representing the requirements for the job.

    employer_data: This is a nested serializer EmployernameSerializer which serializes the employer model
    instance associated with the job.

    is_draft: This is a BooleanField representing whether the job is a draft or not.

    skill: This is a nested serializer RequireskillSerializer that serializes the required skills for the job.
    """

    skill = RequireskillSerializer(many=True)
    category_name = CategorySerializer(source='category')
    employer_data = EmployernameSerializer(source='employer')

    def create(self, validated_data):
        skills = validated_data.pop('skill')
        job = super().create(validated_data)
        for skill in skills:
            instance, created = Required_Skill.objects.get_or_create(skill=skill['skill'])
            job.skill.add(instance)
        return job

    def update(self, instance, validated_data):
        skills = validated_data.pop('skill')
        job = super().update(instance, validated_data)
        job.skill.clear()
        for skill in skills:
            instance, created = Required_Skill.objects.get_or_create(skill=skill['skill'])
            job.skill.add(instance)
        return job

    class Meta:
        model = Job
        fields = [
            'name',
            'description',
            'category_name',
            'budget',
            'duration',
            'requirement',
            'employer_data',
            'is_draft',
            'skill',
        ]


class CategorywiseJobSerializer(serializers.Serializer):
    """This is a Django REST Framework serializer for a model that represents the count of jobs in each category.
    The CategorywiseJobSerializer has two fields:

    category__category: This is a CharField that represents the name of the category. The field name is
    constructed by concatenating the related model name category with the field name category, using a
    double underscore __ as a separator. This field will store the name of the category associated with
    the count of jobs.

    count: This is an IntegerField that represents the count of jobs in the category.
    This field will store an integer value.

    The serializer is used to serialize and deserialize data between Python objects and JSON,
    so it can be used to communicate with an API that returns or accepts data in JSON format.
    When the serializer is used to serialize an instance of the model, it will convert the model
    data into a JSON object that has the same structure as the serializer. Conversely, when the
    serializer is used to deserialize a JSON object, it will convert the JSON data into a Python
    object that has the same structure as the serializer.
    """

    category__category = serializers.CharField()
    count = serializers.IntegerField()


class BidperJobSerializer(serializers.Serializer):

    job__name = serializers.CharField()
    count = serializers.IntegerField()

    # class Meta:
    #     model = Bid
    #     fields = ['job', 'count']


class RateSerializer(serializers.ModelSerializer):
    """This is a Django REST Framework serializer for the Rating model. The RateSerializer
    has a single nested Meta class that defines the model to be serialized and the fields to
    be included in the serialized output. The Meta class specifies the following:

    model: This is the Django model that the serializer is based on, which is Rating.

    fields: This is a list of fields to include in the serialized output. In this case,
    the RateSerializer includes the following fields:

    employer: This is a foreign key to the User model representing the employer who created the rating.
    job_seeker: This is a foreign key to the User model representing the job seeker who received the rating.
    job: This is a foreign key to the Job model representing the job that was rated.
    rating: This is an integer field representing the rating given by the employer to the job seeker.
    feedback: This is a text field allowing the employer to provide feedback to the job seeker about their performance.

    The RateSerializer will convert instances of the Rating model to JSON format when sending them over an API,
    and it will convert JSON data to instances of the Rating model when receiving data from an API. The serializer
    is a more user-friendly way of interacting with the Rating model, as it abstracts away the details of the
    model's implementation and provides a simple interface for working with the data.
    """

    class Meta:
        model = Rating
        fields = ['employer', 'job_seeker', 'job', 'rating', 'feedback']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['job', 'proposal', 'amount', 'job_seeker', 'require_days', 'milestone']


class JobnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['name']


class ShortlistSerializer(serializers.ModelSerializer):
    project = JobnameSerializer(source='job')

    class Meta:
        model = Bid
        fields = ['project', 'job_seeker', 'is_shortlisted']
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['job', 'job_seeker', 'employer', 'is_active', 'is_finished']
