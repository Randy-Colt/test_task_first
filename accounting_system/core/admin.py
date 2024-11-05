from django.contrib import admin

from core import models as core
from core.constants import WASTE_NAMES, LIMITS_NAMES


@admin.register(core.Waste)
class WasteAdmin(admin.ModelAdmin):
    list_display = ('id', *WASTE_NAMES, *LIMITS_NAMES)
    list_filter = WASTE_NAMES
    search_fields = 'id',


@admin.register(core.Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'waste')
    search_fields = 'name',


@admin.register(core.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'waste', 'user')
    search_fields = ('name', 'user')


@admin.register(core.StorageDistance)
class StorageDistanceAdmin(admin.ModelAdmin):
    list_display = ('storage', 'neighbour_storage', 'distance')
    search_fields = 'storage',


@admin.register(core.OrganizationStorageDist)
class OrgStorDistAdmin(admin.ModelAdmin):
    list_display = ('organization', 'storage', 'distance')
    search_fields = ('organization__name', 'storage__name')
