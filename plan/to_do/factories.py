from django.contrib.auth import get_user_model
from factory import sequence
from factory.django import DjangoModelFactory

from to_do.models import ToDo, Organization

User = get_user_model()


def _get_user():
    user = User.objects.first()
    OrganizationFactory()
    return user


def _create_organization():
    organization = OrganizationFactory()
    return organization


class OrganizationFactory(DjangoModelFactory):
    name = 'Personal'

    class Meta:
        model = Organization


class TaskFactory(DjangoModelFactory):
    description = 'description '
    user = _get_user()
    organization = _create_organization()

    @sequence
    def title(self):
        max_id = ToDo.objects.latest('id').id
        return f'title-{max_id + 1}'

    class Meta:
        model = ToDo

