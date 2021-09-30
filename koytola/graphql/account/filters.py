import django_filters

from ...account.models import User, AccountEvent
from ..core.filters import EnumFilter, ListObjectTypeFilter, ObjectTypeFilter
from ..core.types.common import DateRangeInput
from ..utils.filters import filter_by_query_param, filter_range_field
from .enums import AccountStatus, AccountEventsEnum, StaffMemberStatus, UserType


def filter_account(qs, _, value):
    account_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    qs = filter_by_query_param(qs, value, account_fields)
    return qs


def filter_date(qs, _, value):
    return filter_range_field(qs, "date__date", value)


def filter_date_joined(qs, _, value):
    return filter_range_field(qs, "date_joined__date", value)


def filter_date_last_login(qs, _, value):
    return filter_range_field(qs, "last_login__date", value)


def filter_event_type(qs, _, value):
    query_objects = qs.none()
    if value:
        query_objects |= qs.filter(type__in=value)
    return query_objects.distinct()


def filter_user_status(qs, _, value):
    if value == AccountStatus.ACTIVE:
        qs = qs.filter(is_active=True)
    elif value == AccountStatus.INACTIVE:
        qs = qs.filter(is_active=False)
    return qs


def filter_user_type(qs, _, value):
    if value == UserType.SELLER:
        qs = qs.filter(is_staff=True, is_seller=True)
    elif value == UserType.BUYER:
        qs = qs.filter(is_staff=True, is_seller=False)
    return qs


def filter_staff_status(qs, _, value):
    if value == StaffMemberStatus.ACTIVE:
        qs = qs.filter(is_staff=True, is_active=True)
    elif value == StaffMemberStatus.DEACTIVATED:
        qs = qs.filter(is_staff=True, is_active=False)
    return qs


def filter_staff_search(qs, _, value):
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "default_billing_address__first_name",
        "default_billing_address__last_name",
        "default_billing_address__city",
        "default_billing_address__country",
    )
    if value:
        qs = filter_by_query_param(qs, value, search_fields)
    return qs


def filter_search(qs, _, value):
    search_fields = ("name",)
    if value:
        qs = filter_by_query_param(qs, value, search_fields)
    return qs


def filter_search_event(qs, _, value):
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "type",
        "order__user__email",
        "order__user__first_name",
        "order__user__last_name",
        "profile__name",
        "profile__slug",
    )
    if value:
        qs = filter_by_query_param(qs, value, search_fields)
    return qs.distinct()


class AccountFilter(django_filters.FilterSet):
    date_joined = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_joined
    )
    last_login = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date_last_login
    )
    status = EnumFilter(input_class=AccountStatus, method=filter_user_status)
    search = django_filters.CharFilter(method=filter_staff_search)
    type = EnumFilter(input_class=UserType, method=filter_user_type)

    class Meta:
        model = User
        fields = [
            "date_joined",
            "last_login",
            "status",
            "search",
            "type",
        ]


class PermissionGroupFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_search)


class StaffUserFilter(django_filters.FilterSet):
    status = EnumFilter(input_class=StaffMemberStatus, method=filter_staff_status)
    search = django_filters.CharFilter(method=filter_staff_search)

    # TODO - Figure out after permission types
    # department = ObjectTypeFilter

    class Meta:
        model = User
        fields = ["status", "search"]


class EventFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method=filter_account)
    user_type = EnumFilter(input_class=UserType, method=filter_user_type)
    date = ObjectTypeFilter(
        input_class=DateRangeInput, method=filter_date
    )
    type = ListObjectTypeFilter(input_class=AccountEventsEnum, method=filter_event_type)
    search = django_filters.CharFilter(method=filter_search_event)

    class Meta:
        model = AccountEvent
        fields = [
            "user",
            "user_type",
            "date",
            "type",
            "search",
        ]

