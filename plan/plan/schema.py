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
    todos = graphene.List(TodosType, first=graphene.Int(), last=graphene.Int())
    organizations = graphene.List(OrganizationType, first=graphene.Int(), last=graphene.Int())
    users = graphene.List(UserType, first=graphene.Int(), last=graphene.Int())

    def resolve_todos(self, info, first = None, last = None):
        return ToDo.objects.all()[first: last]

    def resolve_organizations(self, info, first = None, last = None):
        return Organization.objects.all()[first: last]

    def resolve_users(self, info, first = None, last = None):
        return User.objects.all()[first: last]


class Mutate(graphene.ObjectType):
    create_todo = CreateToDoMutation.Field()
    create_organization = CreateOrganizationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutate)

