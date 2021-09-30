from django.contrib import admin
from .models import Blog, BlogCategory
from ..core.utils import download_csv


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "id", "slug", "is_published", "title",  "creation_date", "publication_date", "update_date"
    ]
    search_fields = ["slug", "title", "description", "content"]
    list_filter = ["is_published", "creation_date", "publication_date", "update_date"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date"]


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "slug", "parent", "created_at"]


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
