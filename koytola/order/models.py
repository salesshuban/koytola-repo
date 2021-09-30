from operator import attrgetter
from uuid import uuid4

from django.conf import settings
from django.db.models import JSONField, F, Q, Sum
from django.db import models
from django.utils.timezone import now
from django_prices.models import MoneyField, TaxedMoneyField
from prices import Money

from ..account.models import User, Address
from ..core.models import ModelWithMetadata
from ..core.permissions import OrderPermissions
from ..core.taxes import zero_money, zero_taxed_money
from ..core.utils.json_serializer import CustomJsonEncoder
from ..payment import ChargeStatus, TransactionKind
from . import OrderEvents, OrderStatus


class OrderQueryset(models.QuerySet):
    def cancelled(self):
        """Return cancelled orders."""
        return self.filter(status=OrderEvents.CANCELLED)

    def completed(self):
        """Return completed orders."""
        return self.filter(status=OrderEvents.COMPLETED)

    def created(self):
        """Return created orders."""
        return self.filter(status=OrderEvents.CREATED)

    def fulfilled(self):
        """Return fulfilled orders."""
        return self.filter(status=OrderEvents.FULFILLED)

    def paid_all(self):
        """Return paid orders."""
        return self.filter(
            Q(status=OrderEvents.PAID) or Q(status=OrderEvents.MARKED_AS_PAID)
        )

    def paid(self):
        """Return paid orders."""
        return self.filter(status=OrderEvents.PAID)

    def marked_as_paid(self):
        """Return paid orders."""
        return self.filter(status=OrderEvents.MARKED_AS_PAID)

    def ready_to_fulfill(self):
        """Return orders that can be fulfilled.

        Orders ready to fulfill are fully paid but unfulfilled (or partially
        fulfilled in some cases).
        """
        statuses = {OrderStatus.UNFULFILLED}
        qs = self.filter(status__in=statuses, payments__is_active=True)
        qs = qs.annotate(amount_paid=Sum("payments__captured_amount"))
        return qs.filter(total_gross_amount__lte=F("amount_paid"))

    def pending(self):
        """Return pending orders."""
        return self.filter(status=OrderEvents.PENDING)


class Order(ModelWithMetadata):
    created = models.DateTimeField(default=now, editable=False)
    status = models.CharField(
        max_length=32, default=OrderEvents.CREATED, choices=OrderEvents.CHOICES
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="orders",
        on_delete=models.SET_NULL,
    )
    language_code = models.CharField(max_length=35, default=settings.LANGUAGE_CODE)
    billing_address = models.ForeignKey(
        Address, related_name="+", editable=False, null=True, on_delete=models.SET_NULL
    )
    user_email = models.EmailField(blank=True, default="")
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    token = models.CharField(max_length=36, unique=True, blank=True)

    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_net = MoneyField(amount_field="total_net_amount", currency_field="currency")

    total_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_gross = MoneyField(
        amount_field="total_gross_amount", currency_field="currency"
    )

    total = TaxedMoneyField(
        net_amount_field="total_net_amount",
        gross_amount_field="total_gross_amount",
        currency_field="currency",
    )

    note = models.TextField(blank=True, default="")

    objects = OrderQueryset.as_manager()

    class Meta:
        ordering = ("-pk",)
        permissions = ((OrderPermissions.MANAGE_ORDERS.codename, "Manage orders."),)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid4())
        return super().save(*args, **kwargs)

    def is_paid(self):
        if self.status in {OrderEvents.PAID}:
            return True
        else:
            return False

    def get_account_email(self):
        return self.user.email if self.user else self.user_email

    def _index_billing_phone(self):
        return self.billing_address.phone

    def __repr__(self):
        return "<Order #%r>" % (self.id,)

    def __str__(self):
        return "#%d" % (self.id,)

    def get_last_payment(self):
        return max(self.payments.all(), default=None, key=attrgetter("pk"))

    def get_payment_status(self):
        last_payment = self.get_last_payment()
        if last_payment:
            return last_payment.charge_status
        return ChargeStatus.NOT_CHARGED

    def get_payment_status_display(self):
        last_payment = self.get_last_payment()
        if last_payment:
            return last_payment.get_charge_status_display()
        return dict(ChargeStatus.CHOICES).get(ChargeStatus.NOT_CHARGED)

    def is_pre_authorized(self):
        return (
            self.payments.filter(
                is_active=True, transactions__kind=TransactionKind.AUTH
            )
            .filter(transactions__is_success=True)
            .exists()
        )

    def is_captured(self):
        return (
            self.payments.filter(
                is_active=True, transactions__kind=TransactionKind.CAPTURE
            )
            .filter(transactions__is_success=True)
            .exists()
        )

    def get_total(self):
        return sum(self.total, zero_taxed_money())

    def can_capture(self, payment=None):
        if not payment:
            payment = self.get_last_payment()
        if not payment:
            return False
        order_status_ok = self.status not in {OrderEvents.PAID}
        return payment.can_capture() and order_status_ok

    def can_void(self, payment=None):
        if not payment:
            payment = self.get_last_payment()
        if not payment:
            return False
        return payment.can_void()

    def can_refund(self, payment=None):
        if not payment:
            payment = self.get_last_payment()
        if not payment:
            return False
        return payment.can_refund()

    def can_mark_as_paid(self):
        return len(self.payments.all()) == 0

    @property
    def total_authorized(self):
        payment = self.get_last_payment()
        if payment:
            return payment.get_authorized_amount()
        return zero_money()

    @property
    def total_captured(self):
        payment = self.get_last_payment()
        if payment and payment.charge_status in (
            ChargeStatus.PARTIALLY_CHARGED,
            ChargeStatus.FULLY_CHARGED,
            ChargeStatus.PARTIALLY_REFUNDED,
        ):
            return Money(payment.captured_amount, payment.currency)
        return zero_money()

    @property
    def total_balance(self):
        return self.total_captured - self.total.gross


class OrderEvent(models.Model):
    """Model used to store events that happened during the order lifecycle.

    Args:
        parameters: Values needed to display the event on the storefront
        type: Type of an order

    """

    date = models.DateTimeField(default=now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in OrderEvents.CHOICES
        ],
    )
    order = models.ForeignKey(Order, related_name="events", on_delete=models.CASCADE)
    parameters = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        ordering = ("date",)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, user={self.user!r})"
