from rest_framework.generics import ListAPIView

from .serializers import OrganizationSerializer


class ListOrganizationApi(ListAPIView):
    # permission_classes = pass
    serializer_class = OrganizationSerializer

