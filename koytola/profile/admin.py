from django.contrib import admin
from .models import (
    Company,
    Representative,
    Certificate,
    Brochure,
    Video,
    SocialResponsibility,
    Contact,
    Industry,
    CertificateType,
    Images,
    Roetter,
    SuccessStory
)
from ..core.utils import download_csv


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "id", "user", "name", "website", "phone",
        "founded_year", "no_of_employees", "size", "type",
        "is_active", "organic_products", "private_label",
        "female_leadership", "branded_value", "is_verified",
        "is_published", "creation_date", "publication_date",
        "update_date"
    ]
    search_fields = ["username", "name", "website"]
    list_filter = [
        "is_active", "is_published", "is_verified", "size",
        "type", "founded_year", "organic_products",
        "organic_products", "private_label", "female_leadership",
        "branded_value", "creation_date", "publication_date",
        "update_date",
    ]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date", "id"]


class RepresentativeAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company",  "photo", "name", "position", "linkedin_url"
    ]
    search_fields = ["company", "name", "position"]
    list_filter = ["company", "position"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class CertificateAdmin(admin.ModelAdmin):
    list_display = ["id", "company",  "certificate", "type"]
    search_fields = ["company", "description"]
    list_filter = ["company"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class BrochureAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company",  "brochure", "description"
    ]
    search_fields = ["company", "description"]
    list_filter = ["company"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class ImagesAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company",  "image", "description"
    ]
    search_fields = ["company", "description"]
    list_filter = ["company"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class VideoAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company", "description"
    ]
    search_fields = ["company", "description"]
    list_filter = ["company"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class SocialResponsibilityAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company",  "name", "description"
    ]
    search_fields = ["company", "description"]
    list_filter = ["company"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "email", "submission_date", "subject",
        "contact", "type", "status"
    ]
    search_fields = ["name", "email", "subject", "contact"]
    list_filter = ["submission_date", "type", "status", "country"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-submission_date", "id"]


class IndustryAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "is_active", "creation_date", "update_date"]
    search_fields = ["name", ]
    list_filter = ["name", "is_active"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date", "id"]


class CertificateTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "description", "is_active", "creation_date", "update_date"]
    search_fields = ["name", ]
    list_filter = ["name", "is_active"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date", "id"]


class RoetterAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "type", "is_active", "created_at"]
    search_fields = ["name", "category__id", "category__name", "type"]
    list_filter = ["name", "type", "is_active"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["created_at", "id"]


class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "name", "company_name", "slug", "tags", "is_active", 'is_active']
    search_fields = ["title", "name", "company_name", "tags", "is_active", "is_active"]
    list_filter = ["title", "name", "company_name", "tags", "is_active", "is_active"]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["created_at", "id"]


admin.site.register(Industry, IndustryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(CertificateType, CertificateTypeAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Brochure, BrochureAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(SuccessStory, SuccessStoryAdmin)
admin.site.register(SocialResponsibility, SocialResponsibilityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Roetter, RoetterAdmin)
