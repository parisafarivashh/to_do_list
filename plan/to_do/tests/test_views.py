import json
import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from user.models import Token
from to_do.models import Organization, ToDo


User = get_user_model()


class SetUp:

    @pytest.fixture
    def set_up(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='samira',
            password='123456'
        )
        self.access_token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)
        self.organization = Organization.objects.create(name='personal')
        self.organization2 = Organization.objects.create(name='work')
        self.task = ToDo.objects.create(
            organization=self.organization,
            title='new-task',
            description='description',
            date='2022-11-23',
            user=self.user,
        )
        self.task2 = ToDo.objects.create(
            organization=self.organization,
            title='second-task',
            description='description',
            date='2022-11-24',
            user=self.user,
        )


class TestViewToDo(SetUp):

    @pytest.mark.django_db
    def test_task_create(self, set_up):
        data = json.dumps({
            "organization": self.organization.id,
            "title": "task",
            "description": "description",
            "date": '2022-11-21',
        })
        response = self.client.post(
            path='/task/',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert len(response.data) == 6
        assert response.data['id'] is not None
        assert response.data['title'] == 'task'
        assert response.data['date'] == '2022-11-21T00:00:00Z'

    @pytest.mark.django_db
    def test_task_update(self, set_up):
        data = json.dumps({
            "tick": True,
        })
        response = self.client.patch(
            path=f'/task/{self.task.id}',
            data=data,
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.data['tick'] is True
        assert response.data['title'] == self.task.title
        assert response.data['priority'] == self.task.priority
        assert len(response.data) == 5

    @pytest.mark.django_db
    def test_task_get(self, set_up):
        response = self.client.get(path=f'/task/{self.task.id}')
        assert response.status_code == 200
        assert response.data['tick'] is False
        assert response.data['id'] is not None
        assert response.data['title'] == self.task.title
        assert response.data['priority'] == self.task.priority
        assert len(response.data) == 8

    @pytest.mark.django_db
    def test_task_list(self, set_up):
        response = self.client.get(path='/task/')
        assert response.status_code == 200
        assert len(response.data) == 2

        for task in response.data:
            assert task['tick'] is False
            assert task['id'] is not None
            assert task['title'] in [
                self.task.title,
                self.task2.title,
            ]
            assert len(task) == 8

    @pytest.mark.django_db
    def test_task_delete(self, set_up):
        response = self.client.delete(path=f'/task/{self.task2.id}')
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_organization_list(self, set_up):
        response = self.client.get(path='/task/organization')
        assert response.status_code == 200
        assert len(response.data) == 2

        for organization in response.data:
            assert organization['name'] in [
                self.organization.name,
                self.organization2.name,
            ]
            assert len(organization) == 2

