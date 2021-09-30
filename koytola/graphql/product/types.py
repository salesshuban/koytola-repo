import json

import graphene
from graphene import relay
from graphene_federation import key
from ..core.scalars import Array, Json
from ...graphql.utils import get_user_or_app_from_context
from ...product import models
from ..core.connection import CountableDjangoObjectType
from ..core.types import Image, CountryDisplay
from .enums import ProductUnitsEnum
from ..core.fields import FilterInputConnectionField
from .filters import ProductFilterInput
from .sorters import ProductSortingInput
from django.db.models import Avg
from ..core.types.rosetters import Roetter
from ..core.types.certificate_type import CertificateType, Certificate
from ..core.types.rosetters import Roetter
from ...profile import models as pm
from datetime import datetime


class ProductImage(CountableDjangoObjectType):
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Sizes of the product image.")
    )

    class Meta:
        description = (
            "Company product images."
        )
        only_fields = [
            "id",
            "product",
            "image",
            "ppoi",
            "index", 
            "alt_text",
            "order"
        ]
        interfaces = [relay.Node]
        model = models.ProductImage

    @staticmethod
    def resolve_image(root: models.ProductImage, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.alt_text,
                size=size,
                rendition_key_set="products",
                info=info,
            )


class ProductVideo(CountableDjangoObjectType):

    class Meta:
        description = (
            "Company product videos."
        )
        only_fields = [
            "id",
            "product",
            "video",
            "alt_text",
            "order"
        ]
        interfaces = [relay.Node]
        model = models.ProductVideo


class HSCodeAndProduct(CountableDjangoObjectType):

    class Meta:
        description = (
            "HS Code And Product."
        )
        only_fields = [
            "id",
            "hs_code",
            "product_name",
        ]
        interfaces = [relay.Node]
        model = models.HSCodeAndProduct


class ProductReviews(CountableDjangoObjectType):

    class Meta:
        description = (
            "Company product Reviews."
        )
        only_fields = [
            "id",
            "user",
            "product",
            "name",
            "rating",
            "review",
            "location",
            "like",
            "unlike",
            "created_at"
        ]
        interfaces = [relay.Node]
        model = models.ProductReviews


@key("id")
@key("slug")
class Product(CountableDjangoObjectType):
    category = graphene.Field(
        lambda: Category,
        description="Product category."
    )
    images = graphene.List(
        lambda: ProductImage,
        description="Sizes of the product images."
    )
    thumbnail = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Sizes of the product thumbnail.")
    )
    unit = ProductUnitsEnum(description="Product unit type.")
    quantity_unit = ProductUnitsEnum(description="Product quantity unit type.")
    videos = graphene.List(
        lambda: ProductVideo,
        description="List of product videos."
    )
    tags = Array(description="Product`s tags")
    reviews = FilterInputConnectionField(
        lambda: ProductReviews,
        description="product reviews"
    )
    total_review = graphene.Float(description="total review")
    total_ratting = graphene.Float(description="total ratting")
    rosetter = graphene.List(lambda: Roetter, description="Product Certificate rosetter")
    certificate_type = graphene.List(lambda: CertificateType, description="Product Certificate Type")

    class Meta:
        description = (
            "Company product."
        )
        only_fields = [
            "id",
            "company",
            "name",
            "slug",
            "seo_title",
            "seo_description",
            "description",
            "description_plaintext",
            "hs_code",
            "unit_number",
            "unit_price",
            "currency",
            "minimum_order_quantity",
            "organic",
            "private_label",
            "is_active",
            "creation_date",
            "publication_date",
            "update_date",
            "is_published",
            "is_brand",
            "brand",
            "delivery_time_option",
            "delivery_time",
            "packaging",
            "delivery"
        ]
        interfaces = [relay.Node]
        model = models.Product

    @staticmethod
    def resolve_rosetter(root: models.Product, info, **_kwargs):
        return root.rosetter.all()

    @staticmethod
    def resolve_certificate_type(root: models.Product, info, **_kwargs):
        return root.certificate_type.all()

    @staticmethod
    def resolve_tags(root: models.Product, info,  **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_thumbnail(root: models.Product, info, size=None, **_kwargs):
        if root.images:
            return Image.get_adjusted(
                image=root.images[0],
                alt=root.images[0].alt_text,
                size=size,
                rendition_key_set="products",
                info=info,
            )

    @staticmethod
    def resolve_images(root: models.Product, info, **_kwargs):
        return root.images.all().order_by("index")

    @staticmethod
    def resolve_videos(root: models.Product, info, **_kwargs):
        return root.videos.all()

    @staticmethod
    def resolve_category(root: models.Product, info, **_kwargs):
        return root.category

    @staticmethod
    def resolve_reviews(root: models.Product, info, **_kwargs):
        return root.product_review.all()

    @staticmethod
    def resolve_total_review(root: models.Product, info, **_kwargs):
        return len(root.product_review.all())

    @staticmethod
    def resolve_total_ratting(root: models.Product, info, **_kwargs):
        ratting = list(models.ProductReviews.objects.filter(product=root).aggregate(Avg("rating")).values())[0]
        return ratting if ratting else 0


@key("id")
@key("slug")
class Category(CountableDjangoObjectType):
    products = FilterInputConnectionField(
        lambda: Product,
        filter=ProductFilterInput(description="Filtering options for products."),
        sort_by=ProductSortingInput(description="Sort products."),
        description="List of products.",
    )
    children = graphene.List(
        lambda: Category, description="List of children of the category."
    )
    background_image = graphene.Field(
        Image, size=graphene.Int(description="Size of the image.")
    )
    tags = Array(description="Category`s tags")
    product_count = graphene.Int(description="count of the category`s product.")
    rosetter = graphene.List(Roetter, description="product rosetter by categories. ")

    class Meta:
        description = (
            "Product categories."
        )
        only_fields = [
            "id",
            "name",
            "slug",
            "seo_title",
            "seo_description",
            "description",
            "parent",
        ]
        interfaces = [relay.Node]
        model = models.Category

    @staticmethod
    def resolve_rosetter(root: models.Category, info, **_kwargs):
        if pm.Roetter.objects.filter(type="Product", category__icontains=root.name).exists():
            return pm.Roetter.objects.filter(type="Product", category__icontains=root.name)
        else:
            return pm.Roetter.objects.filter(type="Product")

    @staticmethod
    def resolve_tags(root: models.Category, info, **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_background_image(root: models.Category, info, size=None, **_kwargs):
        if root.background_image:
            return Image.get_adjusted(
                image=root.background_image,
                alt=root.background_image_alt,
                size=size,
                rendition_key_set="background_images",
                info=info,
            )

    @staticmethod
    def resolve_children(root: models.Category, info, **_kwargs):
        return root.children.all()

    @staticmethod
    def resolve_products(root: models.Category, info, **_kwargs):
        return models.Product.objects.filter(category__in=root.get_descendants(include_self=True).values_list('pk'))

    @staticmethod
    def resolve_product_count(root: models.Category, info, **_kwargs):
        qs = root.get_descendants(include_self=True)
        return models.Product.objects.filter(category__in=qs).count()


@key("id")
@key("slug")
class Offers(CountableDjangoObjectType):
    categories = graphene.List(
        lambda: Category,
        description="Offers category."
    )
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Offer image sizes.")
    )
    tags = Array(description="Offer`s tags")
    products = graphene.List(Product, description="offer of the products.")
    unit = graphene.String(description="offer of the products.")

    class Meta:
        description = ("Offers.", )
        only_fields = [
            "id",
            "company",
            "user",
            "title",
            "slug",
            "get_code",
            "value",
            "start_date",
            "end_date",
            "is_active"
        ]
        interfaces = [relay.Node]
        model = models.Offers

    @staticmethod
    def resolve_unit(root: models.Offers, info, **_kwargs):
        return root.unit

    @staticmethod
    def resolve_tags(root: models.Offers, info,  **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_image(root: models.Offers, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.title,
                size=size,
                rendition_key_set="images",
                info=info,
            )

    @staticmethod
    def resolve_products(root: models.Offers, info, size=None, **_kwargs):
        return root.products.all()

    @staticmethod
    def resolve_categories(root: models.Offers, info, size=None, **_kwargs):
        return root.categories.all()


class PortProductGallery(CountableDjangoObjectType):
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Sizes of the product image.")
    )

    class Meta:
        description = ("Port Product Gallery.", )
        only_fields = [
            "id",
            "product",
            "image",
            "ppoi",
            "video",
            "is_active",
            "created_at"
        ]
        interfaces = [relay.Node]
        model = models.PortProductGallery

    @staticmethod
    def resolve_image(root: models.PortProductGallery, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.alt_text,
                size=size,
                rendition_key_set="port_product_gallery",
                info=info,
            )


@key("id")
@key("slug")
class PortDeals(CountableDjangoObjectType):
    port_product_gallery = graphene.List(
        lambda: PortProductGallery,
        description="List of products under the category.",
    )
    certificate = Array()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()

    class Meta:
        description = ("Port Deals.", )
        only_fields = [
            "id",
            "company",
            "name",
            "location",
            "lat",
            "lng",
            "slug",
            "product_name",
            "hs_code",
            "quantity",
            "address",
            "unit",
            "container_number",
            "quantity_unit",
            "price",
            "currency",
            "discount_price",
            "discount_percentage",
            "description",
            "is_active",
            "created_at",
            "start_date",
            "end_date",
            "is_expire"
        ]
        interfaces = [relay.Node]
        model = models.PortDeals

    @staticmethod
    def resolve_start_date(root: models.PortDeals, _info):
        if root.start_date:
            return datetime.strptime(root.start_date.strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def resolve_end_date(root: models.PortDeals, _info):
        if root.end_date:
            return datetime.strptime(root.end_date.strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def resolve_port_product_gallery(root: models.PortDeals, _info):
        if root.port_product_gallery:
            return root.port_product_gallery.all()
        else:
            return None

    @staticmethod
    def resolve_certificate(root: models.PortDeals, _info):
        if root.certificate:
            return eval(root.certificate)
        else:
            return []


class ProductQuery(CountableDjangoObjectType):
    country = graphene.Field(
        CountryDisplay, required=True, description="Product Query's default country."
    )

    class Meta:
        description = ("Product Query.", )
        only_fields = [
            "id",
            "email",
            "name",
            "product",
            "quantity",
            "message",
            "offer",
            "is_closed",
            "created_at",
            "updated_at"
        ]
        interfaces = [relay.Node]
        model = models.ProductQuery

    @staticmethod
    def resolve_country(root: models.ProductQuery, _info):
        if root.country.code:
            return CountryDisplay(code=root.country.code, country=root.country.name)
        else:
            return CountryDisplay()


class OpenExchange(CountableDjangoObjectType):
    rates = Json()

    class Meta:
        description = ("Product Query.", )
        only_fields = [
            "id",
            "base",
            "timestamp",
            "rates",
            "created_at",
            "updated_at",
        ]
        interfaces = [relay.Node]
        model = models.OpenExchange

    @staticmethod
    def resolve_country(root: models.OpenExchange, _info):
        return json.loads(root.rates)
