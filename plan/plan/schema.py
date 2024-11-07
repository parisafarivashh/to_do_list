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


class CreateToDoMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    todo = graphene.Field(TodosType)

    def mutate(self, info, title, description):
        todo = ToDo.objects.create(title=title, description=description)
        return CreateToDoMutation(todo=todo)


class CreateOrganizationMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    organization = graphene.Field(OrganizationType)

    def mutate(self, info, name, **kwargs):
        organization = Organization.objects.create(name=name)
        return CreateOrganizationMutation(organization=organization)


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

class Mutate(graphene.ObjectType):
    create_todo = CreateToDoMutation.Field()
    create_organization = CreateOrganizationMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutate)

