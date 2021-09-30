import graphene

from ...graphql.core.enums import to_enum
from ...order import OrderEvents, OrderEventsEmails

OrderEventsEnum = to_enum(OrderEvents)
OrderEventsEmailsEnum = to_enum(OrderEventsEmails)


class OrderStatusFilter(graphene.Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    CREATED = "created"
    FULFILLED = "fulfilled"
    PAID = "paid"
    PENDING = "pending"
