import datetime

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

    def validate_date(self, value):
        if value.date() < datetime.datetime.today().date():
            raise serializers.ValidationError("You Can Not Set Past Time")
        return value


class UpdateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'priority', 'date', 'tick']

    def validate_date(self, value):
        if value.date() < datetime.datetime.today().date():
            raise serializers.ValidationError("You Can Not Set Past Time")
        return value


class RetrieveToDoSerializers(serializers.ModelSerializer):
    user = RetrieveUpdateProfileSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'priority', 'tick', 'date',
                  'user', 'organization']

