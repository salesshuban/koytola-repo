import django_filters

from ...site.models import ContactMessage, SiteSubscriber
from ..core.filters import EnumFilter, ObjectTypeFilter
from ..core.types.common import DateRangeInput
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import ContactMessageStatusEnum, SiteSubscriptionStatus


def filter_contact_messages_search(qs, _, value):
    contact_message_fields = [
        "full_name", "email", "subject", "content"
    ]
    qs = filter_by_query_param(qs, value, contact_message_fields)
    return qs


def filter_contact_messages_status(qs, _, value):
    contact_message_fields = [
        "full_name", "email", "subject", "content"
    ]
    qs = filter_by_query_param(qs, value, contact_message_fields)
    return qs


def filter_date_created(qs, _, value):
    return filter_range_field(qs, "creation_date__date", value)


def filter_date_submitted(qs, _, value):
    return filter_range_field(qs, "date_submitted__date", value)


def filter_date_updated(qs, _, value):
    return filter_range_field(qs, "date_updated__date", value)


def filter_active_status(qs, _, value):
    if value == SiteSubscriptionStatus.ACTIVE:
        qs = qs.filter(is_active=True)
    elif value == SiteSubscriptionStatus.INACTIVE:
        qs = qs.filter(is_active=False)
    return qs


def filter_status(qs, _, value):
    query_objects = qs.none()
    if value:
        query_objects |= qs.filter(status=value)
    return query_objects.distinct()


def filter_subscriber_search(qs, _, value):
    contact_message_fields = ["email"]
    qs = filter_by_query_param(qs, value, contact_message_fields)
    return qs


class ContactMessageFilter(django_filters.FilterSet):
    date_submitted = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_submitted
    )
    date_updated = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_updated
    )
    status = EnumFilter(
        input_class=ContactMessageStatusEnum,
        method=filter_status
    )
    search = django_filters.CharFilter(method=filter_contact_messages_search)

    class Meta:
        model = ContactMessage
        fields = [
            "date_submitted",
            "date_updated",
            "status",
            "search"
        ]


class ContactMessageFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = ContactMessageFilter


class SiteSubscriberFilter(django_filters.FilterSet):
    date_created = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_created
    )
    status = EnumFilter(
        input_class=SiteSubscriptionStatus, method=filter_active_status
    )
    search = django_filters.CharFilter(method=filter_subscriber_search)

    class Meta:
        model = SiteSubscriber
        fields = [
            "date_created",
            "status",
            "search"
        ]


class SiteSubscriberFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = SiteSubscriberFilter
