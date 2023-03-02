from rest_framework import serializers

from src.employer.models import Employer
from src.users.serializers import UsernameSerializer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['user', 'description', 'phone']


class EmployernameSerializer(serializers.ModelSerializer):

    username = UsernameSerializer(source='user')

    class Meta:
        model = Employer
        fields = ['username', 'phone']
