import graphene
from graphene_django import DjangoObjectType

from to_do.models import ToDo, Organization
from user.models import User


class UserType(DjangoObjectType):

    class Meta:
        model = User


class TodosType(DjangoObjectType):
    class Meta:
        model = ToDo


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


class Query(graphene.ObjectType):
    todos = graphene.List(TodosType)
    organizations = graphene.List(OrganizationType)
    users = graphene.List(UserType)

    def resolve_todos(self, info):
        return ToDo.objects.all()

    def resolve_organizations(self, info):
        return Organization.objects.all()

    def resolve_users(self, info):
        return User.objects.all()


schema = graphene.Schema(query=Query)

