from django.contrib import admin
from .models import Payment, Transaction
from ..core.utils import download_csv


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id", "gateway", "is_active", "created", "modified", "charge_status", "total", "currency", "order"
    ]
    search_fields = []
    list_filter = ["gateway", "is_active", "created", "charge_status"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-created"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "created", "payment", "kind", "is_success", "action_required", "amount", "currency"
    ]
    search_fields = ["account_id", "gateway_response"]
    list_filter = ["kind", "created", "is_success"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-created"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction, TransactionAdmin)
