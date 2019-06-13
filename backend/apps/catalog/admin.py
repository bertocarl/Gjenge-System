from django.contrib import admin

from apps.catalog.models import HazardousMaterial


@admin.register(HazardousMaterial)
class HazardousMaterialAdmin(admin.ModelAdmin):
    list_display = ('kind', 'coefficient')
