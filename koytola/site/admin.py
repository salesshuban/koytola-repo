from django.contrib import admin
from .models import (
    SiteSettings,
    SiteSettingsTranslation,
    AuthorizationKey,
    SiteSubscriber,
    Image,
    ContactMessage
)
from ..core.utils import download_csv, download_json


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "id", "site", "header_text", "description", "company_address", "default_mail_sender_name",
        "default_mail_sender_name", "default_mail_sender_address"
    ]
    search_fields = []
    list_filter = []
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["id"]


class SiteSettingsTranslationAdmin(admin.ModelAdmin):
    list_display = ["id", "language_code", "site_settings", "header_text", "description"]
    search_fields = []
    list_filter = []
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["id"]


class AuthorizationKeyAdmin(admin.ModelAdmin):
    list_display = ["id", "site_settings", "name"]
    search_fields = []
    list_filter = []
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["id"]


class SiteSubscriberAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_active", "creation_date"]
    search_fields = ["email"]
    list_filter = ["creation_date", "is_active"]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-creation_date"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", "alt_text", "creation_date", "notes"]
    search_fields = ["image", "notes"]
    list_filter = ["creation_date"]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-creation_date"]


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "date_submitted", "subject", "subject", "date_updated"]
    search_fields = ["full_name", "email", "subject", "content"]
    list_filter = ["date_submitted", "date_updated"]
    actions = [download_csv, download_json]

    def get_ordering(self, request):
        return ["-date_submitted"]


admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(SiteSettingsTranslation, SiteSettingsTranslationAdmin)
admin.site.register(AuthorizationKey, AuthorizationKeyAdmin)
admin.site.register(SiteSubscriber, SiteSubscriberAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
