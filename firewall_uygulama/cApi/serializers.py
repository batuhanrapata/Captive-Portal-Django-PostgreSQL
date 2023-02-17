from .models import User, Log, email_verification
from rest_framework import serializers
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate
from rest_framework import exceptions



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'tc_no', 'birth_date', 'tel_no', 'confirmation', 'email', 'timestamp')

class djangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise exceptions.AuthenticationFailed('Incorrect Credentials')


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('user','email_ver','ip_tables','timestamp')


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = email_verification
        fields = ('user','email_code','confirmation','timestamp')
