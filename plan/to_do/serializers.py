from rest_framework import serializers

from .models import Organization, ToDo


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class CreateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['organization', 'title', 'description', 'priority', 'date']


class UpdateToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'priority', 'date', 'tick']


class RetrieveToDoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'

