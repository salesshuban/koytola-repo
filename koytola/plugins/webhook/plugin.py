from typing import TYPE_CHECKING, Any, Optional

from ...webhook.event_types import WebhookEventType
from ...webhook.payloads import (
    generate_customer_payload,
    generate_invoice_payload,
    generate_order_payload,
)
from ..base_plugin import BasePlugin
from .tasks import trigger_webhooks_for_event

if TYPE_CHECKING:
    from ...order.models import Order
    from ...account.models import User
    from ...invoice.models import Invoice


class WebhookPlugin(BasePlugin):
    PLUGIN_ID = "koytola.webhooks"
    PLUGIN_NAME = "Webhooks"
    DEFAULT_ACTIVE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    def order_created(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_CREATED, order_data)

    def order_fully_paid(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_FULLY_PAID, order_data)

    def order_updated(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_UPDATED, order_data)

    def invoice_request(
        self,
        order: "Order",
        invoice: "Invoice",
        number: Optional[str],
        previous_value: Any,
    ) -> Any:
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(
            WebhookEventType.INVOICE_REQUESTED, invoice_data
        )

    def invoice_delete(self, invoice: "Invoice", previous_value: Any):
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(WebhookEventType.INVOICE_DELETED, invoice_data)

    def invoice_sent(self, invoice: "Invoice", email: str, previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        invoice_data = generate_invoice_payload(invoice)
        trigger_webhooks_for_event.delay(WebhookEventType.INVOICE_SENT, invoice_data)

    def order_cancelled(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_CANCELLED, order_data)

    def order_fulfilled(self, order: "Order", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        order_data = generate_order_payload(order)
        trigger_webhooks_for_event.delay(WebhookEventType.ORDER_FULFILLED, order_data)

    def account_created(self, account: "User", previous_value: Any) -> Any:
        if not self.active:
            return previous_value
        account_data = generate_customer_payload(account)
        trigger_webhooks_for_event.delay(
            WebhookEventType.ACCOUNT_CREATED, account_data
        )
