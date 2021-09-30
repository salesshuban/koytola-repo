import django_filters
from django.db.models import Q

from ...profile.models import Company, SuccessStory
from ..core.filters import EnumFilter, ObjectTypeFilter
from ..core.types import FilterInputObjectType
from ..core.types.common import DateRangeInput
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import (
    ProfileStatus,
    ProfileActivationStatus,
    ProfilePublishedStatus
)


def filter_status(qs, _, value):
    if value:
        if value == ProfileStatus.ACTIVE:
            qs = qs.filter(is_active=True)
        elif value == ProfileStatus.INACTIVE:
            qs = qs.filter(is_active=False)
        elif value == ProfileStatus.PUBLISHED:
            qs = qs.filter(Q(is_active=True) & Q(is_published=True))
        elif value == ProfileStatus.HIDDEN:
            qs = qs.filter(Q(is_active=True) & Q(is_published=False))
    return qs


def filter_active(qs, _, value):
    if value:
        if value == ProfileActivationStatus.ACTIVE:
            qs = qs.filter(is_active=True)
        elif value == ProfileActivationStatus.INACTIVE:
            qs = qs.filter(is_active=False)
    return qs


def filter_published(qs, _, value):
    if value:
        if value == ProfilePublishedStatus.PUBLISHED:
            qs = qs.filter(is_published=True)
        elif value == ProfilePublishedStatus.HIDDEN:
            qs = qs.filter(is_published=False)
    return qs


def filter_date_created(qs, _, value):
    return filter_range_field(qs, "creation_date__date", value)


def success_story_filter_date_created(qs, _, value):
    return filter_range_field(qs, "created_at__date", value)


def filter_search(qs, _, value):
    profile_fields = ["slug", "name", "website", "content"]
    qs = filter_by_query_param(qs, value, profile_fields)
    return qs


def success_story_filter_search(qs, _, value):
    profile_fields = ["slug", "title", "name", "location", "description", "tags"]
    qs = filter_by_query_param(qs, value, profile_fields)
    return qs


class CompanyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_search)
    status = EnumFilter(
        input_class=ProfileStatus,
        method=filter_status
    )
    is_active = EnumFilter(
        input_class=ProfileActivationStatus,
        method=filter_active
    )
    is_published = EnumFilter(
        input_class=ProfilePublishedStatus,
        method=filter_published
    )
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_created
    )

    class Meta:
        model = Company
        fields = [
            "search",
            "status",
            "is_active",
            "is_published",
            "date_created"
        ]


class CompanyFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = CompanyFilter


class SuccessStoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=success_story_filter_search)

    is_active = EnumFilter(
        input_class=ProfileActivationStatus,
        method=filter_active
    )
    is_published = EnumFilter(
        input_class=ProfilePublishedStatus,
        method=filter_published
    )
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=success_story_filter_date_created
    )

    class Meta:
        model = SuccessStory
        fields = [
            "search",
            "title",
            "name",
            "description",
            "location",
            "company_name",
            "slug",
            "tags",
            "is_active",
            "created_at",
            "is_published"
        ]


class SuccessStoryFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = SuccessStoryFilter
