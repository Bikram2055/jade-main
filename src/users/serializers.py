from rest_framework import serializers

from src.users.models import Address, User


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'profile_picture',
        )
        read_only_fields = ('username',)


class CreateUserSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, user):
        return user.get_tokens()

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'tokens',
            'profile_picture',
        )
        read_only_fields = ('tokens',)
        extra_kwargs = {'password': {'write_only': True}}


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user', 'country', 'city', 'street']


class Address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street']
