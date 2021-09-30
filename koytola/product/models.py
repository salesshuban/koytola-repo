from django.conf import settings
from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from versatileimagefield.fields import PPOIField, VersatileImageField
from ..core.db.fields import SanitizedJSONField
from ..core.models import (
    ModelWithMetadata,
    PublishableModel,
    PublishedQuerySet,
)
from ..account.models import User, Address
from ..core.utils.draftjs import json_content_to_raw_text
from ..core.permissions import ProductPermissions
from ..core.utils.editorjs import clean_editor_js
from ..profile.models import (
    Company,
    Industry,
    SuccessStory,
    Roetter,
    CertificateType,
    Certificate,
    Contact,
    SocialResponsibility,
    Brochure,
    Images,
    Representative,
    Video
)
from ..seo.models import SeoModel
from . import ProductUnits, DeliveryTimeOption
from ..core.utils import upload_path_handler
from ..profile.models import Roetter, CertificateType, Certificate
from django_countries.fields import Country, CountryField


class HSCodeAndProduct(models.Model):
    hs_code = models.CharField(max_length=250)
    product_name = models.TextField(blank=True, default="")


class Category(MPTTModel, ModelWithMetadata, SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    description = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    description_plaintext = models.TextField(blank=True, default="")
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = VersatileImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    tags = models.TextField(max_length=25000, blank=True, null=True)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        ordering = ["slug", "name", "pk"]
        permissions = [
            (
                ProductPermissions.MANAGE_CATEGORIES.codename,
                "Manage categories."
            )
        ]

    def __str__(self) -> str:
        return self.name


class Product(SeoModel, ModelWithMetadata, PublishableModel):
    company = models.ForeignKey(Company, related_name="products", on_delete=models.SET_NULL, null=True)
    name = models.TextField(max_length=25000)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    description_plaintext = models.TextField(blank=True, default="")
    hs_code = models.CharField(max_length=32)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    unit_number = models.PositiveIntegerField(default=1, blank=False)
    unit = models.CharField(max_length=32, choices=ProductUnits.CHOICES, blank=ProductUnits.ITEM, null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH, default=settings.DEFAULT_CURRENCY)
    minimum_order_quantity = models.PositiveIntegerField(default=1, blank=False)
    quantity_unit = models.CharField(max_length=32, choices=ProductUnits.CHOICES, blank=ProductUnits.ITEM, null=True)
    organic = models.BooleanField(default=False)
    private_label = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    objects = PublishedQuerySet.as_manager()
    is_brand = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, null=True, blank=True)
    certificate_type = models.ManyToManyField(CertificateType, related_name="product_certificate_type+", blank=True)
    rosetter = models.ManyToManyField(Roetter, related_name="product_rosetter+", blank=True)
    tags = models.TextField(max_length=6550, blank=True, default="[]")
    packaging = models.TextField(max_length=65500, blank=True, null=True)
    delivery = models.TextField(max_length=65500, blank=True, null=True)
    delivery_time_option = models.CharField(max_length=32, choices=DeliveryTimeOption.CHOICES, blank=True, null=True)
    delivery_time = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["slug", "name", "pk"]
        permissions = [
            (
                ProductPermissions.MANAGE_PRODUCTS.codename,
                "Manage products."
            )
        ]

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )

    def __str__(self) -> str:
        return self.name

    @property
    def plain_text_description(self) -> str:
        return json_content_to_raw_text(self.description)

    def get_first_image(self):
        if self.images:
            images = list(self.images.all())
            return images[0] if images else None


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(
        upload_to="products", ppoi_field="ppoi", blank=False
    )
    ppoi = PPOIField()
    alt_text = models.CharField(max_length=128, blank=True)
    index = models.IntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["pk"]


class ProductVideo(models.Model):
    product = models.ForeignKey(
        Product, related_name="videos", on_delete=models.CASCADE
    )
    video = VersatileImageField(
        upload_to="products", ppoi_field="ppoi", blank=False
    )
    alt_text = models.CharField(max_length=128, blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["pk"]


class Offers(models.Model):
    company = models.ForeignKey(Company, related_name="offers_company", on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, related_name="offers_user", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250, blank=True)
    slug = models.CharField(max_length=250, blank=True)
    get_code = models.CharField(max_length=250, blank=True)
    value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    unit = models.CharField(max_length=250, choices=[('%', '%'), ('DIRECT', 'DIRECT')])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tags = models.TextField(max_length=65500, default="[]")
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    products = models.ManyToManyField(Product, related_name="offers_products+", blank=True)
    categories = models.ManyToManyField(Category, related_name="offers_categories+", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class PortDeals(models.Model):
    company = models.ForeignKey(Company, related_name="port_deals_company", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, blank=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    address = models.ForeignKey(
        Address,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    product_name = models.TextField(max_length=25000, blank=True, null=True)
    hs_code = models.CharField(max_length=250)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=32, choices=ProductUnits.CHOICES, blank=ProductUnits.ITEM, null=True)
    quantity_unit = models.CharField(max_length=32, choices=ProductUnits.CHOICES, blank=ProductUnits.ITEM, null=True)
    currency = models.CharField(max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH, default=settings.DEFAULT_CURRENCY)
    price = models.FloatField(default=0.0)
    container_number = models.CharField(max_length=250, blank=True, null=True)
    discount_price = models.FloatField(default=0.0)
    discount_percentage = models.FloatField(default=0.0)
    certificate = models.TextField(max_length=25000, blank=True, null=True)
    description = models.TextField(max_length=65500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_expire = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class PortProductGallery(models.Model):
    product = models.ForeignKey(PortDeals, related_name="port_product_gallery", on_delete=models.CASCADE)
    image = VersatileImageField(upload_to="products/port/", ppoi_field="ppoi", blank=True, null=True)
    ppoi = PPOIField()
    video = VersatileImageField(upload_to="products/port/", ppoi_field="ppoi", blank=True, null=True)
    alt_text = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="product_review_user", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_review")
    name = models.CharField(max_length=250)
    rating = models.FloatField(default=0)
    review = models.TextField(max_length=65500, null=True, blank=True)
    location = models.TextField(max_length=65500, null=True, blank=True)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductQuery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_query")
    offer = models.ForeignKey(Offers, on_delete=models.SET_NULL, related_name="product_query_offer", null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    message = models.TextField(max_length=65500, default="")
    country = CountryField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name


class OpenExchange(models.Model):
    base = models.CharField(max_length=5)
    timestamp = models.DateTimeField()
    rates = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.base
