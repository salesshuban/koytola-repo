import graphene

from ...core.permissions import OrderPermissions
from ..core.enums import ReportingPeriod
from ..core.fields import FilterInputConnectionField, PrefetchingConnectionField
from ..core.scalars import UUID
from ..core.types import FilterInputObjectType, TaxedMoney
from ..decorators import permission_required
from .bulk_mutations.orders import OrderBulkCancel
from .filters import OrderFilter
from .mutations.orders import (
    OrderAddNote,
    OrderCancel,
    OrderCapture,
    OrderMarkAsPaid,
    OrderRefund,
    OrderUpdate,
    OrderVoid,
)
from .resolvers import (
    resolve_order,
    resolve_orders,
)
from .sorters import OrderSortingInput
from .types import Order, OrderEvent


class OrderFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = OrderFilter


class OrderQueries(graphene.ObjectType):
    homepage_events = PrefetchingConnectionField(
        OrderEvent,
        description=(
            "List of activity events to display on "
            "homepage (at the moment it only contains order-events)."
        ),
    )
    order = graphene.Field(
        Order,
        description="Look up an order by ID.",
        id=graphene.Argument(graphene.ID, description="ID of an order.", required=True),
    )
    orders = FilterInputConnectionField(
        Order,
        sort_by=OrderSortingInput(description="Sort orders."),
        filter=OrderFilterInput(description="Filtering options for orders."),
        description="List of orders.",
    )
    orders_total = graphene.Field(
        TaxedMoney,
        description="Return the total sales amount from a specific period.",
        period=graphene.Argument(ReportingPeriod, description="A period of time."),
    )
    order_by_token = graphene.Field(
        Order,
        description="Look up an order by token.",
        token=graphene.Argument(UUID, description="The order's token.", required=True),
    )

    @permission_required(OrderPermissions.MANAGE_ORDERS)
    def resolve_order(self, info, **data):
        return resolve_order(info, data.get("id"))

    @permission_required(OrderPermissions.MANAGE_ORDERS)
    def resolve_orders(self, info, **_kwargs):
        return resolve_orders(info)


class OrderMutations(graphene.ObjectType):
    order_add_note = OrderAddNote.Field()
    order_cancel = OrderCancel.Field()
    order_capture = OrderCapture.Field()
    order_mark_as_paid = OrderMarkAsPaid.Field()
    order_refund = OrderRefund.Field()
    order_update = OrderUpdate.Field()
    order_void = OrderVoid.Field()
    order_bulk_cancel = OrderBulkCancel.Field()
