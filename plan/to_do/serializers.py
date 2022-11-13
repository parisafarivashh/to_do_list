import datetime

import django
from django.utils import timezone
from rest_framework import serializers

from .models import Organization, ToDo
from user.serializers import RetrieveUpdateProfileSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CreateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['organization', 'title', 'description', 'priority',  'date']

    def validate(self, attrs):
        if attrs['date'].date() <= datetime.datetime.today().date():
            raise serializers.ValidationError(
                {'message': "You Can Not Set Past Time"}
            )
        return attrs


class UpdateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'priority', 'date', 'tick']

    def validate(self, attrs):
        if attrs['date'].date() <= datetime.datetime.today().date():
            raise serializers.ValidationError(
                {'message': "You Can Not Set Past Time"}
            )
        return attrs


class RetrieveToDoSerializers(serializers.ModelSerializer):
    user = RetrieveUpdateProfileSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'priority', 'tick', 'date',
                  'user', 'organization']

