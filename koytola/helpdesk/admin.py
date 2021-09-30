from django.contrib import admin
from .models import Ticket
from ..core.utils import download_csv


class HelpdeskAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "type", "user", "subject", "creation_date", "update_date"]
    search_fields = ["status", "type", "user"]
    list_filter = ["status", "type", "creation_date", "update_date"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date"]


admin.site.register(Ticket, HelpdeskAdmin)
