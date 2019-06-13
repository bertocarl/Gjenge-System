from django.contrib.gis.db import models
from django.contrib import admin
from mapwidgets import GooglePointFieldWidget

from apps.api.models import Checkpoint, Transportation, Device, UserProfile


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ('uuid', 'location', 'transportation', 'created_at', 'updated_at', 'data')


@admin.register(Transportation)
class CheckpointAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    list_display = ('pk', 'device', 'start_point', 'end_point', 'status', 'created_at', 'updated_at', 'data')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
