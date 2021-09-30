from django.contrib import admin
from .models import (
    Tracking,
)
from ..core.utils import download_csv, download_json


class TrackingAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user", "date", "type", "category",
        "company", "product", "referrer", "country", "city"
    ]
    search_fields = [
        "ip", "country", "region", "city", "postal",
        "location_details", "referrer", "device", "browser",
        "system"
    ]
    list_filter = ["date"]
    list_per_page = 100
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-date", "-id"]


admin.site.register(Tracking, TrackingAdmin)
