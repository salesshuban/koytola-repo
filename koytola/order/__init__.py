class OrderStatus:
    DRAFT = "draft"  # fully editable, not confirmed order created by staff users
    UNFULFILLED = "unfulfilled"  # order with no items marked as fulfilled
    FULFILLED = "fulfilled"  # order with all items marked as fulfilled
    CANCELLED = "cancelled"  # permanently cancelled order

    CHOICES = [
        (DRAFT, "Draft"),
        (UNFULFILLED, "Unfulfilled"),
        (FULFILLED, "Fulfilled"),
        (CANCELLED, "Canceled"),
    ]


class FulfillmentStatus:
    FULFILLED = "fulfilled"  # group of products in an order marked as fulfilled
    CANCELLED = "cancelled"  # fulfilled group of products in an order marked as cancelled

    CHOICES = [
        (FULFILLED, "Fulfilled"),
        (CANCELLED, "Cancelled"),
    ]


class OrderEvents:
    """The different order event types."""
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    CREATED = "created"
    FULFILLED = "fulfilled"
    PAID = "paid"
    PENDING = "pending"

    MARKED_AS_PAID = "marked_as_paid"

    EMAIL_SENT = "email_sent"

    PAYMENT_AUTHORIZED = "payment_authorized"
    PAYMENT_CAPTURED = "payment_captured"
    PAYMENT_REFUNDED = "payment_refunded"
    PAYMENT_VOIDED = "payment_voided"
    PAYMENT_FAILED = "payment_failed"
    EXTERNAL_SERVICE_NOTIFICATION = "external_service_notification"

    INVOICE_REQUESTED = "invoice_requested"
    INVOICE_GENERATED = "invoice_generated"
    INVOICE_UPDATED = "invoice_updated"
    INVOICE_SENT = "invoice_sent"

    NOTE_ADDED = "note_added"

    # Used mostly for importing legacy data from before Enum-based events
    OTHER = "other"

    CHOICES = [
        (CANCELLED, "The order was cancelled"),
        (COMPLETED, "The order was completed"),
        (CREATED, "The order was created"),
        (FULFILLED, "The order was fulfilled"),
        (PAID, "The order was paid"),
        (PENDING, "The order was pending"),
        (MARKED_AS_PAID, "The order was manually marked as fully paid"),
        (EMAIL_SENT, "The email was sent"),
        (PAYMENT_AUTHORIZED, "The payment was authorized"),
        (PAYMENT_CAPTURED, "The payment was captured"),
        (PAYMENT_REFUNDED, "The payment was refunded"),
        (PAYMENT_VOIDED, "The payment was voided"),
        (PAYMENT_FAILED, "The payment was failed"),
        (EXTERNAL_SERVICE_NOTIFICATION, "Notification from external service"),
        (INVOICE_REQUESTED, "An invoice was requested"),
        (INVOICE_GENERATED, "An invoice was generated"),
        (INVOICE_UPDATED, "An invoice was updated"),
        (INVOICE_SENT, "An invoice was sent"),
        (NOTE_ADDED, "A note was added to the order"),
        (OTHER, "An unknown order event containing a message"),
    ]


class OrderEventsEmails:
    """The different order emails event types."""

    PAYMENT = "payment_confirmation"
    ORDER_CONFIRMATION = "order_confirmation"
    ORDER_CANCEL = "order_cancel"
    ORDER_REFUND = "order_refund"
    FULFILLMENT = "fulfillment_confirmation"
    DIGITAL_LINKS = "digital_links"

    CHOICES = [
        (PAYMENT, "The payment confirmation email was sent"),
        (ORDER_CONFIRMATION, "The order placement confirmation email was sent"),
        (ORDER_CANCEL, "The order cancel confirmation email was sent"),
        (ORDER_REFUND, "The order refund confirmation email was sent"),
        (FULFILLMENT, "The fulfillment confirmation email was sent"),
        (DIGITAL_LINKS, "The email containing the digital links was sent"),
    ]
