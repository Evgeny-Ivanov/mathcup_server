from rest_framework import serializers
from .models import User


class SignUpStep1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class SignUpStep2Serializer(serializers.ModelSerializer):
    confirmation_key = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirmation_key')


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ('email', 'password')


class CurrentUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'is_staff')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar')
