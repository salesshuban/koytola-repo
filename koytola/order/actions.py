import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import transaction

from ..payment import ChargeStatus, PaymentError, CustomPaymentChoices
from ..plugins.manager import get_plugins_manager
from . import OrderEvents, OrderEventsEmails, events
from .emails import send_payment_confirmation

if TYPE_CHECKING:
    from .models import Order
    from ..account.models import User
    from ..payment.models import Payment


logger = logging.getLogger(__name__)


def order_created(order: "Order", user: "User"):
    events.order_created_event(order=order, user=user)
    manager = get_plugins_manager()
    manager.order_created(order)
    payment = order.get_last_payment()
    if payment:
        if order.is_captured():
            order_captured(
                order=order, user=user, amount=payment.total, payment=payment
            )
        elif order.is_pre_authorized():
            order_authorized(
                order=order, user=user, amount=payment.total, payment=payment
            )
        if order.is_paid():
            handle_fully_paid_order(order=order, user=user)


def handle_fully_paid_order(order: "Order", user: "User" = None):
    events.order_paid_event(order=order, user=user)

    if order.get_account_email():
        events.email_sent_event(
            order=order, user=user, email_type=OrderEventsEmails.PAYMENT
        )
        send_payment_confirmation.delay(order.pk)

    manager = get_plugins_manager()
    manager.order_paid(order)
    manager.order_updated(order)


@transaction.atomic
def cancel_order(order: "Order", user: "User"):
    """Cancel order.

    Release allocation of unfulfilled order items.
    """

    events.order_canceled_event(order=order, user=user)

    order.status = OrderEvents.CANCELLED
    order.save(update_fields=["status"])

    manager = get_plugins_manager()
    manager.order_cancelled(order)
    manager.order_updated(order)


def order_refunded(order: "Order", user: "User", amount: "Decimal", payment: "Payment"):
    events.payment_refunded_event(
        order=order, user=user, amount=amount, payment=payment
    )
    get_plugins_manager().order_updated(order)


def order_voided(order: "Order", user: "User", payment: "Payment"):
    events.payment_voided_event(order=order, user=user, payment=payment)
    get_plugins_manager().order_updated(order)


def order_authorized(
    order: "Order", user: "User", amount: "Decimal", payment: "Payment"
):
    events.payment_authorized_event(
        order=order, user=user, amount=amount, payment=payment
    )
    get_plugins_manager().order_updated(order)


def order_captured(order: "Order", user: "User", amount: "Decimal", payment: "Payment"):
    events.payment_captured_event(
        order=order, user=user, amount=amount, payment=payment
    )
    get_plugins_manager().order_updated(order)


@transaction.atomic
def mark_order_as_paid(order: "Order", request_user: "User"):
    """Mark order as paid.

    Allows to create a payment for an order without actually performing any
    payment by the gateway.
    """
    # pylint: disable=cyclic-import
    from ..payment.utils import create_payment

    payment = create_payment(
        gateway=CustomPaymentChoices.MANUAL,
        payment_token="",
        currency=order.total.gross.currency,
        email=order.user_email,
        total=order.total.gross.amount,
        order=order,
    )
    payment.charge_status = ChargeStatus.FULLY_CHARGED
    payment.captured_amount = order.total.gross.amount
    payment.save(update_fields=["captured_amount", "charge_status", "modified"])

    events.order_paid_event(order=order, user=request_user)
    manager = get_plugins_manager()
    manager.order_paid(order)
    manager.order_updated(order)


def clean_mark_order_as_paid(order: "Order"):
    """Check if an order can be marked as paid."""
    if order.payments.exists():
        raise PaymentError("Orders with payments can not be manually marked as paid.")
