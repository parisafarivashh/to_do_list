from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from ..views import SignUpView, SignInView, ChangePasswordView

User = get_user_model()


class TestViewUser(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_SignUp(self):
        detail_user = json.dumps({'username': 'sara', 'password': '12345678'})
        request = self.factory.post(
            '/sign-up',
            detail_user,
            content_type='application/json'
        )
        response = SignUpView.as_view()(request)

        assert len(response.data) == 2
        assert response.status_code == 200
        assert response.data['username'] == 'sara'

    def test_SignIn(self):
        self.user = User.objects.create_user(
            username='samira',
            password='123456'
        )

        detail_user = json.dumps({
            'username': self.user.username,
            'password': '123456',
        })

        request = self.factory.post(
            '/sign-in',
            detail_user,
            content_type='application/json'
        )
        response = SignInView.as_view()(request)

        assert response.status_code == 200
        assert response.data['token'] is not None

    def test_change_password(self):
        self.user = User.objects.create_user(
            username='samira',
            password='123456'
        )

        detail_user = json.dumps({
            'username': self.user.username,
            'new_password': 'new_password',
            'repeat_password': 'new_password',
        })
        request = self.factory.put(
            '/change-password',
            detail_user,
            content_type='application/json'
        )
        response = ChangePasswordView.as_view()(request)

        assert response.status_code == 200
        assert response.data['message'] == 'Password Changed Successfully'

