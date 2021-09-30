from typing import Union

from django.contrib.auth.models import _user_has_perm  # type: ignore
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.db.models import JSONField  # type: ignore
from django.db.models import Q, QuerySet, Value
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.crypto import get_random_string
from django_countries.fields import Country, CountryField
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from versatileimagefield.fields import VersatileImageField

from ..core.models import ModelWithMetadata
from ..core.permissions import AccountPermissions, BasePermissionEnum, get_permissions
from ..core.utils.json_serializer import CustomJsonEncoder
from . import AccountEvents
from .validators import validate_possible_number


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class AddressQueryset(models.QuerySet):
    def annotate_default(self, user):
        # Set default shipping/billing address pk to None
        # if default shipping/billing address doesn't exist
        default_shipping_address_pk, default_billing_address_pk = None, None
        if user.default_shipping_address:
            default_shipping_address_pk = user.default_shipping_address.pk
        if user.default_billing_address:
            default_billing_address_pk = user.default_billing_address.pk

        return user.addresses.annotate(
            user_default_shipping_address_pk=Value(
                default_shipping_address_pk, models.IntegerField()
            ),
            user_default_billing_address_pk=Value(
                default_billing_address_pk, models.IntegerField()
            ),
        )


class Countries(models.Model):
    code = models.CharField(max_length=64, blank=True, default="")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    flag = models.FileField(upload_to="Country-flag", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    address_name = models.CharField(max_length=64, blank=True, default="")
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True, null=True)
    street_address_2 = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    city_area = models.CharField(max_length=128, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    country_area = models.CharField(max_length=128, blank=True, null=True)
    phone = PhoneNumberField(max_length=128, blank=True, null=True)

    objects = AddressQueryset.as_manager()

    class Meta:
        ordering = ["address_name", "pk"]

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        if self.company_name:
            return "%s - %s" % (self.company_name, self.full_name)
        return self.full_name

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data() == other.as_data()

    __hash__ = models.Model.__hash__

    def as_data(self):
        """Return the address as a dict suitable for passing as kwargs.

        Result does not contain the primary key or an associated user.
        """
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        if isinstance(data["phone"], PhoneNumber):
            data["phone"] = data["phone"].as_e164
        return data

    def get_copy(self):
        """Return a new instance of the same address."""
        return Address.objects.create(**self.as_data())


class UserManager(BaseUserManager):
    def create_user(
            self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def accounts(self):
        return self.get_queryset().filter(Q(is_staff=False))

    def buyers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) & Q(is_seller=False)
        )

    def sellers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) & Q(is_seller=True)
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(PermissionsMixin, ModelWithMetadata, AbstractBaseUser):
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=12, default=get_random_string, unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    addresses = models.ManyToManyField('Address', blank=True, related_name="user_addresses")
    phone = PossiblePhoneNumberField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    default_shipping_address = models.ForeignKey(
        'Address', related_name="default_shipping_address", null=True, blank=True, on_delete=models.SET_NULL
    )
    default_billing_address = models.ForeignKey(
        'Address', related_name="default_billing_address", null=True, blank=True, on_delete=models.SET_NULL
    )
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    linkedin_url = models.URLField(null=True, blank=True)
    jwt_token_key = models.CharField(max_length=24, default=get_random_string)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ("email",)
        permissions = (
            (AccountPermissions.MANAGE_USERS.codename, "Manage accounts."),
            (AccountPermissions.MANAGE_STAFF.codename, "Manage staff."),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effective_permissions = None

    @property
    def effective_permissions(self) -> "QuerySet[Permission]":
        if self._effective_permissions is None:
            self._effective_permissions = get_permissions()
            if not self.is_superuser:
                self._effective_permissions = self._effective_permissions.filter(
                    Q(user=self) | Q(group__user=self)
                )
        return self._effective_permissions

    @effective_permissions.setter
    def effective_permissions(self, value: "QuerySet[Permission]"):
        self._effective_permissions = value
        # Drop cache for authentication backend
        self._effective_permissions_cache = None

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        if self.default_billing_address:
            first_name = self.default_billing_address.first_name
            last_name = self.default_billing_address.last_name
            if first_name or last_name:
                return ("%s %s" % (first_name, last_name)).strip()
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm: Union[BasePermissionEnum, str], obj=None):  # type: ignore
        # This method is overridden to accept perm as BasePermissionEnum
        perm = perm.value if hasattr(perm, "value") else perm  # type: ignore

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser and not self._effective_permissions:
            return True
        return _user_has_perm(self, perm, obj)


class AccountEvent(models.Model):
    """Model used to store events that happened during the account lifecycle."""

    user = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in AccountEvents.CHOICES
        ],
    )

    # customs = models.ForeignKey("logistics.Custom", on_delete=models.SET_NULL, blank=True, null=True)
    helpdesk = models.ForeignKey("helpdesk.Ticket", on_delete=models.SET_NULL, blank=True, null=True)
    invoice = models.ForeignKey("invoice.Invoice", on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey("order.Order", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey("payment.Payment", on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey("product.Product", on_delete=models.SET_NULL, blank=True, null=True)
    profile = models.ForeignKey("profile.Company", on_delete=models.SET_NULL, blank=True, null=True)
    # shipping = models.ForeignKey("logistics.Shipping", on_delete=models.SET_NULL, blank=True, null=True)
    # shipping_quote = models.ForeignKey("logistics.ShippingQuote", on_delete=models.SET_NULL, blank=True, null=True)

    parameters = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)

    class Meta:
        ordering = ["date"]
        permissions = (
            (
                AccountPermissions.MANAGE_ACCOUNT_EVENTS.codename,
                "Manage account events"
            ),
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, user={self.user!r})"


class StaffNotificationRecipient(models.Model):
    user = models.OneToOneField(
        User,
        related_name="staff_notification",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    staff_email = models.EmailField(unique=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("staff_email",)

    def get_email(self):
        return self.user.email if self.user else self.staff_email
