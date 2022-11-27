from django.contrib.auth import get_user_model
from factory import PostGenerationMethodCall, sequence
from factory.django import DjangoModelFactory


User = get_user_model()


class UserFactory(DjangoModelFactory):
    password = PostGenerationMethodCall('set_password', 'secretIsPassword')

    @sequence
    def username(self):
        max_id = User.objects.latest('id').id
        return f'User-{max_id + 1}'

    class Meta:
        model = User
        django_get_or_create = ['username']

