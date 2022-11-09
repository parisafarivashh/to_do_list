from django.urls import path

from .views import ListOrganizationApi, ToDoView

urlpatterns = [
    path('organization', ListOrganizationApi.as_view(), name='organization_list'),
    path('', ToDoView.as_view(), name='create_todo_view'),
    path('<int:id>', ToDoView.as_view(), name='todo_view'),
]
