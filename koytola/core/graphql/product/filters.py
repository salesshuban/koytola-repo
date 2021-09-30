import django_filters
from django.db.models import Q, Count, Exists, Subquery
import graphene
from django.db.models.expressions import RawSQL
from ...product.models import Product, PortDeals, ProductReviews
from ..core.filters import EnumFilter, ObjectTypeFilter, ListObjectTypeFilter
from ..core.types import FilterInputObjectType
from ..core.types.common import DateRangeInput, IntRangeInput
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import (
    ProductStatus,
    ProductActivationStatus,
    ProductPublishedStatus
)
from ...profile.models import Roetter, CertificateType


def filter_status(qs, _, value):
    if value:
        if value == ProductStatus.ACTIVE:
            qs = qs.filter(is_active=True)
        elif value == ProductStatus.INACTIVE:
            qs = qs.filter(is_active=False)
        elif value == ProductStatus.PUBLISHED:
            qs = qs.filter(Q(is_active=True) & Q(is_published=True))
        elif value == ProductStatus.HIDDEN:
            qs = qs.filter(Q(is_active=True) & Q(is_published=False))
    return qs


def filter_active(qs, _, value):
    if value:
        if value == ProductActivationStatus.ACTIVE:
            qs = qs.filter(is_active=True)
        elif value == ProductActivationStatus.INACTIVE:
            qs = qs.filter(is_active=False)
    return qs


def filter_published(qs, _, value):
    if value:
        if value == ProductPublishedStatus.PUBLISHED:
            qs = qs.filter(is_published=True)
        elif value == ProductPublishedStatus.HIDDEN:
            qs = qs.filter(is_published=False)
    return qs


def filter_date_created(qs, _, value):
    return filter_range_field(qs, "creation_date__date", value)


def filter_price(qs, _, value):
    return filter_range_field(qs, "unit_price", value)


def deal_filter_price(qs, _, value):
    return filter_range_field(qs, "price", value)


def filter_search(qs, _, value):
    product_fields = ["name", "slug", "hs_code"]
    qs = filter_by_query_param(qs, value, product_fields)
    return qs


def filter_rosetter(qs, _, value):
    return qs.filter(rosetter__in=Roetter.objects.filter(name__in=value)).annotate(dcount=Count('id')).order_by()


def filter_certificate_type(qs, _, value):
    return qs.filter(certificate_type__in=CertificateType.objects.filter(name__in=value))


def filter_rating(qs, _, value):
    below = Count('product_review__rating', filter=Q(product_review__rating__in=[float(value), ]))
    return qs.annotate(below=below)


def filter_category(qs, _, value):
    value = [graphene.Node.from_global_id(i)[1] for i in value]
    return qs.filter(category__pk__in=value).annotate(dcount=Count('id')).order_by()


def filter_company(qs, _, value):
    value = [graphene.Node.from_global_id(i)[1] for i in value]
    return qs.filter(company__pk__in=value).annotate(dcount=Count('id')).order_by()


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_search)
    status = EnumFilter(
        input_class=ProductStatus,
        method=filter_status
    )
    is_active = EnumFilter(
        input_class=ProductActivationStatus,
        method=filter_active
    )
    is_published = EnumFilter(
        input_class=ProductPublishedStatus,
        method=filter_published
    )
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_created
    )
    rosetter = ListObjectTypeFilter(input_class=graphene.String, method=filter_rosetter)
    certificate_type = ListObjectTypeFilter(input_class=graphene.String, method=filter_certificate_type)
    rating = django_filters.CharFilter(method=filter_rating)
    price = ObjectTypeFilter(input_class=IntRangeInput, method=filter_price)
    category = ListObjectTypeFilter(input_class=graphene.ID, method=filter_category)
    company = ListObjectTypeFilter(input_class=graphene.ID, method=filter_company)

    class Meta:
        model = Product
        fields = [
            "search",
            "status",
            "is_active",
            "date_created"
        ]


class PortDealsFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_search)
    is_active = EnumFilter(
        input_class=ProductActivationStatus,
        method=filter_active
    )
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_created
    )
    price = ObjectTypeFilter(input_class=IntRangeInput, method=deal_filter_price)
    company = ListObjectTypeFilter(input_class=graphene.ID, method=filter_company)

    class Meta:
        model = PortDeals
        fields = [
            "search",
            "is_active",
            "date_created"
        ]


class ProductFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = ProductFilter


class PortDealsFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = PortDealsFilter
