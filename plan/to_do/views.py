from rest_framework import mixins
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Organization, ToDo
from .serializers import OrganizationSerializer, CreateToDoSerializers, \
    UpdateToDoSerializers, RetrieveToDoSerializers


class ListOrganizationApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class ToDoView(GenericAPIView, mixins.CreateModelMixin,
               mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateToDoSerializers
        elif self.request.method == 'PATCH':
            return UpdateToDoSerializers
        else:
            return RetrieveToDoSerializers

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)
