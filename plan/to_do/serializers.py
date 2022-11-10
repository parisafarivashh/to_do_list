from rest_framework import serializers

from .models import Organization, ToDo
from user.serializers import GetUserDetailSerializer


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CreateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['organization', 'title', 'description', 'priority',  'date']


class UpdateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'priority', 'date', 'tick']


class RetrieveToDoSerializers(serializers.ModelSerializer):
    user = GetUserDetailSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'priority', 'tick', 'date',
                  'user', 'organization']

