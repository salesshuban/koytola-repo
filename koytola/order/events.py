from decimal import Decimal
from typing import Dict, Optional, Union

from ..account import events as account_events
from ..account.models import User
from ..order.models import Order
from ..payment.models import Payment
from . import OrderEvents, OrderEventsEmails
from .models import OrderEvent

UserType = Optional[User]


def _lines_per_quantity_to_line_object_list(quantities_per_order_line):
    return [
        {"quantity": quantity, "line_pk": line.pk, "item": str(line)}
        for quantity, line in quantities_per_order_line
    ]


def _get_payment_data(amount: Optional[Decimal], payment: Payment) -> Dict:
    return {
        "parameters": {
            "amount": amount,
            "payment_id": payment.token,
            "payment_gateway": payment.gateway,
        }
    }


def _user_is_valid(user: UserType) -> bool:
    return bool(user and not user.is_anonymous)


def email_sent_event(
    *,
    order: Order,
    user: Optional[UserType],
    email_type: str,  # use "OrderEventsEmails" class
    user_pk: int = None,
) -> OrderEvent:

    if user and not user.is_anonymous:
        kwargs: Dict[str, Union[User, int]] = {"user": user}
    elif user_pk:
        kwargs = {"user_id": user_pk}
    else:
        kwargs = {}

    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.EMAIL_SENT,
        parameters={"email": order.get_account_email(), "email_type": email_type},
        **kwargs,
    )


def invoice_requested_event(*, order: Order, user: Optional[UserType],) -> OrderEvent:
    return OrderEvent.objects.create(
        order=order, type=OrderEvents.INVOICE_REQUESTED, user=user
    )


def invoice_generated_event(
    *, order: Order, user: Optional[UserType], invoice_number: str,
) -> OrderEvent:
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.INVOICE_GENERATED,
        user=user,
        parameters={"invoice_number": invoice_number},
    )


def invoice_updated_event(
    *,
    order: Order,
    user: Optional[UserType],
    invoice_number: str,
    url: str,
    status: str
) -> OrderEvent:
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.INVOICE_UPDATED,
        user=user,
        parameters={"invoice_number": invoice_number, "url": url, "status": status},
    )


def invoice_sent_event(
    *, order: Order, user: Optional[UserType], email: str,
) -> OrderEvent:
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.INVOICE_SENT,
        user=user,
        parameters={"email": email},
    )


def email_resent_event(
    *, order: Order, user: UserType, email_type: OrderEventsEmails
) -> OrderEvent:
    raise NotImplementedError


def order_created_event(
    *, order: Order, user: UserType, from_draft=False
) -> OrderEvent:
    if from_draft:
        event_type = OrderEvents.CREATED
    else:
        event_type = OrderEvents.CREATED
        account_events.account_order_event(user=user, order=order)

    if not _user_is_valid(user):
        user = None

    return OrderEvent.objects.create(order=order, type=event_type, user=user)


def order_canceled_event(*, order: Order, user: UserType) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(order=order, type=OrderEvents.CANCELLED, user=user)


def order_paid_event(*, order: Order, user: UserType) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(
        order=order, type=OrderEvents.PAID, user=user
    )


def payment_authorized_event(
    *, order: Order, user: UserType, amount: Decimal, payment: Payment
) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.PAYMENT_AUTHORIZED,
        user=user,
        **_get_payment_data(amount, payment),
    )


def payment_captured_event(
    *, order: Order, user: UserType, amount: Decimal, payment: Payment
) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.PAYMENT_CAPTURED,
        user=user,
        **_get_payment_data(amount, payment),
    )


def payment_refunded_event(
    *, order: Order, user: UserType, amount: Decimal, payment: Payment
) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.PAYMENT_REFUNDED,
        user=user,
        **_get_payment_data(amount, payment),
    )


def payment_voided_event(
    *, order: Order, user: UserType, payment: Payment
) -> OrderEvent:
    if not _user_is_valid(user):
        user = None
    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.PAYMENT_VOIDED,
        user=user,
        **_get_payment_data(None, payment),
    )


def payment_failed_event(
    *, order: Order, user: UserType, message: str, payment: Payment
) -> OrderEvent:

    if not _user_is_valid(user):
        user = None
    parameters = {"message": message}

    if payment:
        parameters.update({"gateway": payment.gateway, "payment_id": payment.token})

    return OrderEvent.objects.create(
        order=order, type=OrderEvents.PAYMENT_FAILED, user=user, parameters=parameters
    )


def order_note_added_event(*, order: Order, user: UserType, message: str) -> OrderEvent:
    kwargs = {}
    if user is not None and not user.is_anonymous:
        if order.user is not None and order.user.pk == user.pk:
            account_events.account_added_to_note_order_event(user=user, order=order, message=message)
        kwargs["user"] = user

    return OrderEvent.objects.create(
        order=order,
        type=OrderEvents.NOTE_ADDED,
        parameters={"message": message},
        **kwargs,
    )
