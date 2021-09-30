from django.contrib import admin
from .models import Menu, MenuItem
from ..core.utils import download_csv


class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_filter = []
    list_per_page = 50
    actions = [download_csv]

    def get_ordering(self, request):
        return ["name"]


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["id", "menu", "name", "parent", "url", "page"]
    search_fields = ["menu", "name", "url"]
    list_filter = []
    list_per_page = 50
    actions = [download_csv]

    def get_ordering(self, request):
        return ["id"]


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
