from django.contrib import admin
from .models import News, NewsTranslation
from ..core.utils import download_csv, download_json


class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "slug", "summary", "is_published",
        "creation_date", "publication_date", "update_date"
    ]
    search_fields = ["title", "slug", "summary", "content"]
    list_filter = [
        "is_published", "creation_date", "publication_date",
        "update_date"
    ]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-creation_date"]


class NewsTranslationAdmin(admin.ModelAdmin):
    list_display = [
        "id", "news", "language_code", "title", "summary"
    ]
    search_fields = ["title", "summary", "content"]
    list_filter = ["language_code"]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(News, NewsAdmin)
admin.site.register(NewsTranslation, NewsTranslationAdmin)
