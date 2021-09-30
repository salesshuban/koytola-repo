import django_filters

from ...news.models import News
from ..core.filters import EnumFilter, ObjectTypeFilter
from ..core.types.common import DateRangeInput
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import (
    NewsAudienceTypeEnum,
    NewsPublishedStatus
)


def filter_audience(qs, _, value):
    query_objects = qs.none()
    if value:
        query_objects |= qs.filter(audience=value)
    return query_objects.distinct()


def filter_date_created(qs, _, value):
    return filter_range_field(qs, "creation_date__date", value)


def filter_news_search(qs, _, value):
    news_fields = ["content", "slug", "title", "summary"]
    qs = filter_by_query_param(qs, value, news_fields)
    return qs


def filter_published(qs, _, value):
    if value:
        if value == NewsPublishedStatus.PUBLISHED:
            qs = qs.filter(is_published=True)
        elif value == NewsPublishedStatus.HIDDEN:
            qs = qs.filter(is_published=False)
    return qs


def filter_date_updated(qs, _, value):
    return filter_range_field(qs, "update_date__date", value)


class NewsFilter(django_filters.FilterSet):
    audience = EnumFilter(
        input_class=NewsAudienceTypeEnum,
        method=filter_audience
    )
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_created
    )
    is_published = EnumFilter(
        input_class=NewsPublishedStatus,
        method=filter_published
    )
    search = django_filters.CharFilter(method=filter_news_search)

    class Meta:
        model = News
        fields = [
            "audience",
            "date_created",
            "is_published",
            "search"
        ]


class NewsFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = NewsFilter
