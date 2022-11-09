from django.urls import path

from .views import ListOrganizationApi

urlpatterns = [
    path('organization', ListOrganizationApi.as_view(), name='organization_list'),
]
