from django.contrib import admin
from .models import Invoice, InvoiceEvent
from ..core.utils import download_csv


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "number", "created", "external_url"]
    search_fields = ["order", "external_url"]
    list_filter = ["created"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-created"]


class InvoiceEventAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "type", "order", "user", "parameters"]
    search_fields = ["type", "order", "user", "parameters"]
    list_filter = ["date", "type"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-date"]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceEvent, InvoiceEventAdmin)
