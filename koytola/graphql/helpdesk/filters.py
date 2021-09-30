import django_filters

from ...helpdesk.models import Ticket
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_ticket_search(qs, _, value):
    ticket_fields = ["user", "type", "subject", "content"]
    qs = filter_by_query_param(qs, value, ticket_fields)
    return qs


class TicketFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_ticket_search)

    class Meta:
        model = Ticket
        fields = ["search"]


class TicketFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = TicketFilter
