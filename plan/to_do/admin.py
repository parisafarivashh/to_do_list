from django.contrib import admin

from .models import Organization, ToDo


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']


@admin.register(ToDo)
class ToDoOAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'priority',
        'tick',
        'date',
        'organization_id',
        'organization_title',
        'user_id',
        'user_name',
    ]
    list_filter = [
        'id',
        'title',
        'description',
        'priority',
        'tick',
        'date',
        'organization__id',
        'organization__name',
        'user_id',
        'user__username',
    ]
    search_fields = [
        'id',
        'title',
        'description',
        'priority',
        'tick',
        'date',
        'organization__id',
        'organization__name',
        'user__id',
        'user__username',
    ]
    readonly_fields = [
        'id',
        'title',
        'description',
        'priority',
        'tick',
        'date',
        'organization',
        'user',
    ]

    def user_name(self, obj):
        return obj.user.username

    def user_id(self, obj):
        return obj.user.id

    def organization_id(self, obj):
        return obj.organization.id

    def organization_title(self, obj):
        return obj.organization.name

