from django.contrib import admin
from .models import PluginConfiguration
from ..core.utils import download_csv


class PluginConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "identifier", "name", "description", "active", "configuration"]
    search_fields = ["identifier", "name", "description", "configuration"]
    list_filter = ["active", "identifier"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["identifier"]


admin.site.register(PluginConfiguration, PluginConfigurationAdmin)
