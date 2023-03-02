from rest_framework import serializers

from src.job_seeker.models import Job_Seeker, Skill


class SeekerSkillSerializer(serializers.ModelSerializer):
    """This is a serializer class in Django Rest Framework (DRF). It serializes the Skill model
    and only the skill field is included in the serialized representation. This serializer will
     convert the Skill model instance into a Python dictionary that can be easily converted into
     other data formats, such as JSON or XML. When used with a view in DRF, this serializer will
     allow the Skill model to be displayed in a specified format when accessed via the API.
    """

    class Meta:
        model = Skill
        fields = ['skill']


class Job_SeekerSerializer(serializers.ModelSerializer):
    """This is also a serializer class in Django Rest Framework (DRF). It serializes the Job_Seeker
     model and includes several fields in the serialized representation: user, education, experience,
      phone, and skill. The skill field is a serialized representation of the Skill model, serialized
       using the SeekerSkillSerializer class.

    The many=True argument in the skill field indicates that this field is a many-to-many relationship,
    meaning a Job_Seeker instance can have multiple Skill instances associated with it.
    """

    skill = SeekerSkillSerializer(many=True)

    def create(self, validated_data):
        skills = validated_data.pop('skill')
        job_seeker = super().create(validated_data)
        for skill in skills:
            instance, created = Skill.objects.get_or_create(skill=skill['skill'])
            job_seeker.skill.add(instance)
        return job_seeker

    def update(self, instance, validated_data):
        skills = validated_data.pop('skill')
        job_seeker = super().update(instance, validated_data)
        job_seeker.skill.clear()
        for skill in skills:
            instance, created = Skill.objects.get_or_create(skill=skill['skill'])
            job_seeker.skill.add(instance)
        return job_seeker

    class Meta:
        model = Job_Seeker
        # depth = 1
        fields = ['user', 'education', 'experience', 'phone', 'skill']
