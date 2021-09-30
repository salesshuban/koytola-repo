from django.contrib import admin
from .models import Order, OrderEvent
from ..core.utils import download_csv


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "created", "status", "user", "total", "currency"]
    search_fields = ["user", "billing_address"]
    list_filter = ["created", "status"]
    list_per_page = 50
    ordering = ["-created"]
    actions = [download_csv]


class OrderEventAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "type", "order", "user"]
    search_fields = ["date", "type", "order", "user", "parameters"]
    list_filter = ["date", "type"]
    list_per_page = 50
    ordering = ["-date"]
    actions = [download_csv]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderEvent, OrderEventAdmin)
