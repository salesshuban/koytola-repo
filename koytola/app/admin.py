from django.contrib import admin
from .models import App, AppToken
from ..core.utils import download_csv


class AppAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "is_active", "type", "identifier", "about_app", "version"]
    search_fields = ["name", "type", "about_app"]
    list_filter = ["created", "is_active", "permissions"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["name"]


class AppTokenAdmin(admin.ModelAdmin):
    list_display = ["id", "app", "name", "auth_token"]
    search_fields = ["app", "name"]
    list_filter = []
    actions = [download_csv]

    def get_ordering(self, request):
        return ["app"]


admin.site.register(App, AppAdmin)
admin.site.register(AppToken, AppTokenAdmin)
