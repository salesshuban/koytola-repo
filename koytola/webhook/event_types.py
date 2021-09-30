from ..core.permissions import (
    AccountPermissions,
    OrderPermissions,
)


class WebhookEventType:
    ANY = "any_events"
    ACCOUNT_CREATED = "account_created"

    INVOICE_REQUESTED = "invoice_requested"
    INVOICE_DELETED = "invoice_deleted"
    INVOICE_SENT = "invoice_sent"

    ORDER_CREATED = "order_created"
    ORDER_PAID = "order_paid"
    ORDER_UPDATED = "order_updated"
    ORDER_CANCELLED = "order_cancelled"

    DISPLAY_LABELS = {
        ANY: "Any events",
        ACCOUNT_CREATED: "Account created",
        INVOICE_REQUESTED: "Invoice requested",
        INVOICE_DELETED: "Invoice deleted",
        INVOICE_SENT: "Invoice sent",
        ORDER_CREATED: "Order created",
        ORDER_PAID: "Order paid",
        ORDER_UPDATED: "Order updated",
        ORDER_CANCELLED: "Order cancelled",
    }

    CHOICES = [
        (ANY, DISPLAY_LABELS[ANY]),
        (ACCOUNT_CREATED, DISPLAY_LABELS[ACCOUNT_CREATED]),
        (INVOICE_REQUESTED, DISPLAY_LABELS[INVOICE_REQUESTED]),
        (INVOICE_DELETED, DISPLAY_LABELS[INVOICE_DELETED]),
        (INVOICE_SENT, DISPLAY_LABELS[INVOICE_SENT]),
        (ORDER_CREATED, DISPLAY_LABELS[ORDER_CREATED]),
        (ORDER_PAID, DISPLAY_LABELS[ORDER_PAID]),
        (ORDER_UPDATED, DISPLAY_LABELS[ORDER_UPDATED]),
        (ORDER_CANCELLED, DISPLAY_LABELS[ORDER_CANCELLED]),
    ]

    PERMISSIONS = {
        ACCOUNT_CREATED: AccountPermissions.MANAGE_USERS,
        INVOICE_REQUESTED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_DELETED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_SENT: OrderPermissions.MANAGE_ORDERS,
        ORDER_CREATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_PAID: OrderPermissions.MANAGE_ORDERS,
        ORDER_UPDATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_CANCELLED: OrderPermissions.MANAGE_ORDERS,
    }
