from rest_framework import mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Organization, ToDo
from .serializers import OrganizationSerializer, CreateToDoSerializers, \
    UpdateToDoSerializers, RetrieveToDoSerializers


class ListOrganizationApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()


class ToDoView(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
               mixins.DestroyModelMixin, mixins.UpdateModelMixin,
               GenericAPIView):

    permission_classes = [IsAuthenticated]
    queryset = ToDo.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveToDoSerializers
        elif self.request.method == 'PATCH':
            return UpdateToDoSerializers

    def post(self, request):
        serializer = CreateToDoSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data
        ToDo.objects.create(**obj)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return NotFound

    def patch(self, request, id=None):
        return self.update(request, id, partial=True)

    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            return NotFound

