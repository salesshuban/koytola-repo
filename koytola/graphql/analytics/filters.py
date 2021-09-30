import django_filters
from graphene_django.filter import GlobalIDMultipleChoiceFilter

from ...analytics.models import Tracking
from ...account.models import User
from ...profile.models import Company
from ..core.filters import ListObjectTypeFilter, ObjectTypeFilter
from ..core.types import FilterInputObjectType
from ..core.types.common import DateRangeInput
from ..utils import get_nodes
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import TrackingTypeEnum


def filter_date(qs, _, value):
    return filter_range_field(qs, "date__date", value)


def filter_search(qs, _, value):
    fields = [
        "user__email", "user__first_name", "user__last_name",
        "company__slug", "company__name", "company__content",
        "ip", "country", "region", "city", "postal", "location_details",
        "referrer", "device", "device_type", "browser", "system",
        "parameters", "private_metadata", "metadata"
    ]
    qs = filter_by_query_param(qs, value, fields)
    return qs


def filter_type(qs, _, value):
    query_objects = qs.none()
    if value:
        query_objects |= qs.filter(type__in=value)
    return qs & query_objects


def filter_companies(qs, _, value):
    if value:
        companies = get_nodes(value, "Company", Company)
        qs = qs.filter(company__in=companies)
    return qs


def filter_users(qs, _, value):
    if value:
        users = get_nodes(value, "User", User)
        qs = qs.filter(user__in=users)
    return qs


class TrackingFilter(django_filters.FilterSet):
    date = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date
    )
    search = django_filters.CharFilter(method=filter_search)
    type = ListObjectTypeFilter(
        input_class=TrackingTypeEnum,
        method=filter_type
    )
    companies = GlobalIDMultipleChoiceFilter(method=filter_companies)
    users = GlobalIDMultipleChoiceFilter(method=filter_users)

    class Meta:
        model = Tracking
        fields = [
            "date",
            "search",
            "type",
            "companies",
            "users",
        ]


class TrackingFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = TrackingFilter


class UserTrackingFilter(django_filters.FilterSet):
    date = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date
    )
    type = ListObjectTypeFilter(
        input_class=TrackingTypeEnum,
        method=filter_type
    )

    class Meta:
        model = Tracking
        fields = [
            "date",
            "type",
        ]


class UserTrackingFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = UserTrackingFilter
