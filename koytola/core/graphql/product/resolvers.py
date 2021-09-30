import graphene
from django.db.models import Q, Count, Subquery, Avg, Value, IntegerField, CharField, F
from django.db.models.functions import Coalesce
import requests
from django.db.models.expressions import RawSQL
from ...product.models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    HSCodeAndProduct,
    Offers,
    PortDeals,
    PortProductGallery,
    ProductReviews,
    ProductQuery,
    OpenExchange
)
from ...core.exceptions import PermissionDenied
from ...core.permissions import ProductPermissions
from ..core.validators import validate_one_of_args_is_in_query
from ..utils.filters import filter_by_query_param
from ...profile.models import Roetter, CertificateType
from datetime import datetime


CATEGORY_SEARCH_FIELDS = ("name",)


def resolve_category(info, category_id=None, slug=None):
    validate_one_of_args_is_in_query("id", category_id, "slug", slug)

    if category_id:
        _model, category_pk = graphene.Node.from_global_id(category_id)
        return Category.objects.filter(id=category_pk).first()
    if slug:
        return Category.objects.filter(slug=slug).first()


def resolve_currency_exchange(info, base, **kwargs):
    url = 'https://openexchangerates.org/api/latest.json'
    data = requests.get(url, params={"app_id": "52b0e42121c84181815a8d97e6eef9b8"}).json()
    base = "TRY"
    data['base'] = base
    for currency in data['rates']:
        if currency == base:
            data['rates']['USD'] = 1 / data['rates'][base]
            continue
        data['rates'][currency] = data['rates'][currency] / data['rates'][base]
    timestamp = datetime.fromtimestamp(data['timestamp'])
    if not OpenExchange.objects.filter(base=base).exists():
        OpenExchange(base=base, timestamp=timestamp, rates=data['rates']).save()
    else:
        OpenExchange.objects.filter(base=base).update(timestamp=timestamp, rates=data['rates'],
                                                      updated_at=datetime.now())
    return OpenExchange.objects.filter(base=base).first()


def resolve_categories(info, query, **_kwargs):
    qs = Category.objects.filter(parent=None)
    return filter_by_query_param(qs, query, CATEGORY_SEARCH_FIELDS)


def resolve_product(info, product_id=None, slug=None):
    assert product_id or slug, "No product ID or slug provided."
    # user = info.context.user
    if slug is not None:
        return Product.objects.filter(
            Q(slug=slug) & Q(is_active=True)
        ).first()
    else:
        _model, product_pk = graphene.Node.from_global_id(product_id)
        if product_id is not None:
            # if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
            return Product.objects.filter(pk=product_pk).first()
            # else:
            #     product = Product.objects.filter(
            #         Q(company__user=user) & Q(pk=product_pk)
            #     ).first()
            #     if product:
            #         return product
    raise PermissionDenied()


def resolve_products(info, company_id=None, **_kwargs):
    user = info.context.user
    if company_id:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return Product.objects.filter(company__pk=company_pk).order_by("name")
    if user and not user.is_anonymous and not user.is_superuser:
        return Product.objects.filter(company__user=user).order_by("name")
    else:
        return Product.objects.all().order_by("name")


def resolve_search_hscode_and_product(info, key, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return HSCodeAndProduct.objects.filter(Q(hs_code__contains=key) | Q(product_name__contains=key))
    raise PermissionDenied()


def resolve_product_image(info, product_image_id=None):
    assert product_image_id, "No product image ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_image_pk = graphene.Node.from_global_id(product_image_id)
        if product_image_id is not None:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductImage.objects.filter(pk=product_image_pk).first()
            else:
                product_image = ProductImage.objects.filter(pk=product_image_pk).first()
                if product_image.product.company.is_published and product_image.product.company.is_active:
                    return product_image
    raise PermissionDenied()


def resolve_product_images(info, **_kwargs):
    product_id = _kwargs.get("product_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not product_id:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductImage.objects.all().order_by("index")
        else:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(pk=product_pk).order_by("index").first()
                return product.images
            else:
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(Q(company__user=user) & Q(pk=product_pk)).order_by("index").first()
                if product.company.is_published and product.company.is_active:
                    return product.images
    raise PermissionDenied()


def resolve_product_video(info, product_video_id=None):
    assert product_video_id, "No product video ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_video_pk = graphene.Node.from_global_id(product_video_id)
        if product_video_id is not None:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductVideo.objects.filter(pk=product_video_pk).first()
            else:
                product_video = ProductImage.objects.filter(pk=product_video_pk).first()
                if product_video.product.company.is_published and product_video.product.company.is_active:
                    return product_video
    raise PermissionDenied()


def resolve_product_videos(info, **_kwargs):
    product_id = _kwargs.get("product_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not product_id:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductVideo.objects.all()
        else:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(pk=product_pk).first()
                return product.videos
            else:
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(Q(company__user=user) & Q(pk=product_pk)).first()
                if product.company.is_published and product.company.is_active:
                    return product.videos
    raise PermissionDenied()


def resolve_offer(info, offer_id=None, slug=None):
    assert offer_id or slug, "No product ID or slug provided."
    if slug is not None:
        return Offers.objects.filter(slug=slug, is_active=True).first()
    else:
        _model, offer_pk = graphene.Node.from_global_id(offer_id)
        return Offers.objects.filter(id=offer_pk, is_active=True).first()


def resolve_offers(info, company_id=None, **_kwargs):
    if company_id is not None:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return Offers.objects.filter(company__id=company_pk, is_active=True, end_date__gte=datetime.now()).order_by("-created_at")
    if info.context.user.is_anonymous or info.context.user.is_superuser:
        return Offers.objects.filter(is_active=True, end_date__gte=datetime.now()).order_by("-created_at")
    else:
        return Offers.objects.filter(company__user=info.context.user, is_active=True, end_date__gte=datetime.now()).order_by("-created_at")


def resolve_port_deal(info, id=None, slug=None):
    assert id or slug, "No product ID or slug provided."
    if slug is not None:
        return PortDeals.objects.filter(slug=slug).first()
    else:
        _model, offer_pk = graphene.Node.from_global_id(id)
        return PortDeals.objects.filter(id=offer_pk).first()


def resolve_port_deals(info, company_id=None, **_kwargs):
    PortDeals.objects.filter(end_date__lte=datetime.now(), is_expire=False).update(is_expire=True)
    if company_id is not None:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return PortDeals.objects.filter(company__id=company_pk).order_by("-created_at")
    if info.context.user.is_anonymous or info.context.user.is_superuser:
        return PortDeals.objects.filter(is_active=True, end_date__gte=datetime.now()).order_by("-created_at")
    else:
        return PortDeals.objects.filter(company__user=info.context.user).order_by("-created_at")


def resolve_search_product(info, key, **kwargs):
    if Product.objects.filter(Q(hs_code__icontains=key) | Q(name__icontains=key)).exists():
        field = 'hs_code' if key.isnumeric() else 'name'
        table = Product.objects.model._meta.db_table
        if not info.context.user.is_anonymous and not info.context.user.is_superuser and info.context.user.is_seller:
            query = f"SELECT MAX(id)  FROM {table} WHERE company_id=%s AND {field} iLIKE %s GROUP By {field}"
            return Product.objects.filter(id__in=RawSQL(query, (info.context.user.companies.id, f'%{key}%',)))
        else:
            query = f"SELECT MAX(id)  FROM {table} WHERE {field} iLIKE %s GROUP By {field}"
            return Product.objects.filter(id__in=RawSQL(query, (f'%{key}%',)))
    else:
        return []


def resolve_search_port_deals(info, key, **kwargs):
    return PortDeals.objects.filter(
        Q(slug__contains=key) |
        Q(location__contains=key) |
        Q(company__name__contains=key) |
        Q(product_name__contains=key) |
        Q(hs_code__contains=key) |
        Q(name__contains=key) |
        Q(certificate__contains=key) |
        Q(start_date__contains=key) |
        Q(end_date__contains=key)
    ).annotate(dcount=Count('id')).order_by()


def resolve_product_reviews(info, product_id, **kwargs):
    return ProductReviews.objects.filter(product__id=product_id)


def resolve_product_rosetters(info, **_kwargs):
    return Roetter.objects.filter(type="Product", is_active=True)


def resolve_product_certificate_type(info, **_kwargs):
    return CertificateType.objects.filter(type="Product", is_active=True)


def resolve_product_queries(info, company_id=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if company_id is not None:
            _model, company_pk = graphene.Node.from_global_id(company_id)
            return ProductQuery.objects.filter(product__company__id=company_pk)
        else:
            return ProductQuery.objects.filter(user=user)
    return PermissionDenied()


def resolve_product_query(info, id=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_query_pk = graphene.Node.from_global_id(id)
        return ProductQuery.objects.filter(id=product_query_pk).first()
    return PermissionDenied()


def resolve_port_product_gallery(info, port_deal_id=None, **_kwargs):
    _model, port_deal_pk = graphene.Node.from_global_id(port_deal_id)
    return PortProductGallery.objects.filter(product__id=port_deal_pk)
