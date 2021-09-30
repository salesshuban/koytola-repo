import json
from typing import Optional

from django.db.models import QuerySet

from ..account.models import User
from ..core.utils.anonymization import (
    anonymize_order,
    generate_fake_user,
)
from ..invoice.models import Invoice
from ..order import OrderEvents
from ..order.models import Order
from .event_types import WebhookEventType
from .payload_serializers import PayloadSerializer

ADDRESS_FIELDS = (
    "first_name",
    "last_name",
    "company_name",
    "street_address_1",
    "street_address_2",
    "city",
    "city_area",
    "postal_code",
    "country",
    "country_area",
    "phone",
)

ORDER_FIELDS = (
    "created",
    "status",
    "user_email",
    "total",
    "private_metadata",
    "metadata",
)


def generate_order_payload(order: "Order"):
    serializer = PayloadSerializer()
    payment_fields = (
        "gateway",
        "payment_method_type",
        "cc_brand",
        "is_active",
        "created",
        "modified",
        "charge_status",
        "total",
        "currency",
        "billing_email",
        "billing_first_name",
        "billing_last_name",
        "billing_company_name",
        "billing_address_1",
        "billing_address_2",
        "billing_city",
        "billing_city_area",
        "billing_postal_code",
        "billing_country_code",
        "billing_country_area",
    )
    order_data = serializer.serialize(
        [order],
        fields=ORDER_FIELDS,
        additional_fields={
            "payments": (lambda o: o.payments.all(), payment_fields),
            "billing_address": (lambda o: o.billing_address, ADDRESS_FIELDS),
        },
    )
    return order_data


def generate_invoice_payload(invoice: "Invoice"):
    serializer = PayloadSerializer()
    invoice_fields = ("id", "number", "external_url", "created")
    return serializer.serialize(
        [invoice],
        fields=invoice_fields,
        additional_fields={"order": (lambda i: i.order, ORDER_FIELDS)},
    )


def generate_customer_payload(customer: "User"):
    serializer = PayloadSerializer()
    data = serializer.serialize(
        [customer],
        fields=[
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "private_metadata",
            "metadata",
        ],
        additional_fields={
            "default_shipping_address": (
                lambda c: c.default_billing_address,
                ADDRESS_FIELDS,
            ),
            "default_billing_address": (
                lambda c: c.default_shipping_address,
                ADDRESS_FIELDS,
            ),
        },
    )
    return data


def _get_sample_object(qs: QuerySet):
    """Return random object from query."""
    random_object = qs.order_by("?").first()
    return random_object


def _generate_sample_order_payload(event_name):
    order_qs = Order.objects.prefetch_related(
        "payments",
        "billing_address",
    )
    order = None
    if event_name == WebhookEventType.ORDER_CREATED:
        order = _get_sample_object(order_qs.filter(status=OrderEvents.PENDING))
    elif event_name == WebhookEventType.ORDER_PAID:
        order = _get_sample_object(order_qs.filter(status=OrderEvents.PAID))
    elif event_name in [
        WebhookEventType.ORDER_CANCELLED,
        WebhookEventType.ORDER_UPDATED,
    ]:
        order = _get_sample_object(order_qs.filter(status=OrderEvents.CANCELLED))
    if order:
        anonymized_order = anonymize_order(order)
        return generate_order_payload(anonymized_order)


def generate_sample_payload(event_name: str) -> Optional[dict]:
    if event_name == WebhookEventType.ACCOUNT_CREATED:
        user = generate_fake_user()
        payload = generate_customer_payload(user)
    else:
        payload = _generate_sample_order_payload(event_name)
    return json.loads(payload) if payload else None
