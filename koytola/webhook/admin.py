from django.contrib import admin
from .models import Webhook, WebhookEvent
from ..core.utils import download_csv


class WebhookAdmin(admin.ModelAdmin):
    list_display = ["id", "app", "name", "target_url", "is_active"]
    search_fields = ["app", "name", "target_url"]
    list_filter = ["is_active"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["name"]


class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ["id", "webhook"]
    search_fields = ["webhook"]
    list_filter = []
    actions = [download_csv]

    def get_ordering(self, request):
        return ["id"]


admin.site.register(Webhook, WebhookAdmin)
admin.site.register(WebhookEvent, WebhookEventAdmin)
