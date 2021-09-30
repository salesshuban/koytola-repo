from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    HSCodeAndProduct,
    Offers,
    PortDeals,
    PortProductGallery,
    ProductReviews,
    OpenExchange
)
from ..core.utils import download_csv
from django.contrib.admin import SimpleListFilter


class CategoryFilter(SimpleListFilter):
    title = 'Two Level Categories'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return [('parent', 'parent')]

    def queryset(self, request, queryset):
        cats = Category.objects.none()
        for i in Category.objects.filter(parent=None):
            cats |= i.get_children()
        return cats


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "slug", "description", "parent"
    ]
    search_fields = ["name", "slug", "description", "parent__name"]
    list_filter = ()
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["name", "-id"]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id", "company", "name", "slug", "description", "hs_code",
        "category", "is_published", "unit_number", "unit",
        "minimum_order_quantity", "unit_price", "currency",
        "organic", "private_label", "is_active"
    ]
    search_fields = ["name", "slug", "description"]
    list_filter = [
        "company", "is_published", "is_active", "hs_code",
        "organic", "private_label", "unit_number",
        "creation_date", "publication_date", "update_date"
    ]
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-creation_date", "id"]


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = [
        "id", "product", "unit_price", "currency"
    ]
    search_fields = ["product"]
    list_filter = []
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = [
        "id", "product", "image", "alt_text", "order"
    ]
    search_fields = ["product", "alt_text"]
    list_filter = []
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class ProductVideoAdmin(admin.ModelAdmin):
    list_display = [
        "id", "product", "video", "alt_text", "order"
    ]
    search_fields = ["product", "alt_text"]
    list_filter = []
    list_per_page = 100
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class HSCodeAndProductAdmin(admin.ModelAdmin):
    list_display = ["id", "hs_code", "product_name"]
    search_fields = ["id", "hs_code", "product_name"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


class ProductReviewsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "name", "rating"]
    search_fields = ["id", "user", "product", "name", "rating"]
    actions = [download_csv]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVideo, ProductVideoAdmin)
admin.site.register(HSCodeAndProduct, HSCodeAndProductAdmin)
admin.site.register(Offers)
admin.site.register(OpenExchange)
admin.site.register(PortDeals)
admin.site.register(PortProductGallery)
admin.site.register(ProductReviews, ProductReviewsAdmin)
