from django.contrib import admin
from .models import (
    Address,
    User,
    AccountEvent,
    StaffNotificationRecipient,
    Countries
)
from ..core.utils import download_csv


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "id", "address_name", "first_name", "last_name", "company_name",
        "country", "phone"
    ]
    search_fields = ["address_name", "company_name", "country"]
    list_filter = []
    list_per_page = 50
    actions = [download_csv]

    def get_ordering(self, request):
        return ["id"]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id", "email", "is_superuser", "is_staff", "user_id", "first_name", "last_name",
        "phone", "is_active", "note", "date_joined"
    ]
    search_fields = ["email", "user_id", "first_name", "last_name", "jwt_token_key"]
    list_filter = ["is_superuser", "is_staff", "is_active", "date_joined"]
    list_per_page = 50
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-date_joined"]


class AccountEventAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "type", "user"]
    search_fields = ["type", "user"]
    list_filter = ["date", "type"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-date"]


class StaffNotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "staff_email", "active"]
    search_fields = ["user", "staff_email"]
    list_filter = ["active"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class CountriesAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "latitude", "longitude", "flag", "created_at"]
    search_fields = ["code", "code", "latitude", "longitude"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(Countries, CountriesAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AccountEvent, AccountEventAdmin)
admin.site.register(StaffNotificationRecipient, StaffNotificationRecipientAdmin)
