from django.contrib import admin
from .models import Page, PageType
from ..core.utils import download_csv, download_json


class PageAdmin(admin.ModelAdmin):
    list_display = [
        "id", "slug", "is_published", "title", "summary", "creation_date", "publication_date", "update_date"
    ]
    search_fields = ["slug", "title", "summary", "content"]
    list_filter = ["is_published", "creation_date", "publication_date", "update_date"]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-creation_date"]


class PageTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "name"]
    search_fields = ["slug", "name"]
    list_filter = []
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["slug"]


admin.site.register(Page, PageAdmin)
admin.site.register(PageType, PageTypeAdmin)
