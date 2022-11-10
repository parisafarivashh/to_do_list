from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'photo']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    repeat_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ['username', 'new_password', 'repeat_password']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['repeat_password']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match"}
            )
        return attrs

    def update(self,  instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class GetUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'photo']

