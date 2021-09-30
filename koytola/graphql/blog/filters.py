import django_filters

from ...blog.models import Blog
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_blog_search(qs, _, value):
    blog_fields = ["content", "slug", "title", "summary"]
    qs = filter_by_query_param(qs, value, blog_fields)
    return qs


class BlogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_blog_search)

    class Meta:
        model = Blog
        fields = ["search"]


class BlogFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = BlogFilter
