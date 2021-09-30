import graphene
from django.contrib.auth import get_user_model, models as auth_models
from graphene import relay
from graphene_federation import key

from ...account import models
from ...core.exceptions import PermissionDenied
from ...core.permissions import AccountPermissions, OrderPermissions
from ..core.connection import CountableDjangoObjectType
from ..core.fields import PrefetchingConnectionField
from ..core.types import CountryDisplay, Image, Permission
from ..core.utils import from_global_id_strict_type
from ..decorators import one_of_permissions_required, permission_required
from ..meta.types import ObjectWithMetadata
from ..utils import format_permissions_for_display
from .enums import CountryCodeEnum, AccountEventsEnum
from .utils import can_user_manage_group, get_groups_which_user_can_manage
from ..profile.types import Company
from ...profile import models as profile_models


class AddressInput(graphene.InputObjectType):
    address_name = graphene.String(description="Given name.", required=False)
    first_name = graphene.String(description="Given name.", required=False)
    last_name = graphene.String(description="Family name.", required=False)
    company_name = graphene.String(description="Company or organization.", required=False)
    street_address_1 = graphene.String(description="Address.", required=False)
    street_address_2 = graphene.String(description="Address.", required=False)
    city = graphene.String(description="City.", required=False)
    city_area = graphene.String(description="District.", required=False)
    postal_code = graphene.String(description="Postal code.", required=False)
    country = CountryCodeEnum(description="Country.", required=False)
    country_area = graphene.String(description="State or province.", required=False)
    phone = graphene.String(description="Phone number.", required=False)


@key(fields="id")
@key(fields="code")
class Countries(CountableDjangoObjectType):
    flag = graphene.Field(Image, size=graphene.Int(description="Size of the avatar."))
    
    class Meta:
        description = "Represents user address data."
        interfaces = [relay.Node]
        model = models.Countries
        only_fields = [
            "code",
            "latitude",
            "longitude",
            "name",
            "flag"
            ]

    @staticmethod
    def resolve_flag(root: models.Countries, info, size=None, **_kwargs):
        if root.flag:
            return Image.get_adjusted(
                image=root.flag,
                alt=None,
                size=size,
                rendition_key_set="country_flag",
                info=info,
            )
        
        
@key(fields="id")
class Address(CountableDjangoObjectType):
    country = graphene.Field(
        CountryDisplay, required=True, description="Shop's default country."
    )
    is_default_shipping_address = graphene.Boolean(
        required=False, description="Address is user's default shipping address."
    )
    is_default_billing_address = graphene.Boolean(
        required=False, description="Address is user's default billing address."
    )

    class Meta:
        description = "Represents user address data."
        interfaces = [relay.Node]
        model = models.Address
        only_fields = [
            "address_name",
            "city",
            "city_area",
            "company_name",
            "country",
            "country_area",
            "first_name",
            "id",
            "last_name",
            "phone",
            "postal_code",
            "street_address_1",
            "street_address_2",
        ]

    @staticmethod
    def resolve_country(root: models.Address, _info):
        if root.country.code:
            return CountryDisplay(code=root.country.code, country=root.country.name)
        else:
            return CountryDisplay()

    @staticmethod
    def resolve_is_default_shipping_address(root: models.Address, _info):
        """Look if the address is the default shipping address of the user.

        This field is added through annotation when using the
        `resolve_addresses` resolver. It's invalid for
        `resolve_default_shipping_address` and
        `resolve_default_billing_address`
        """
        if not hasattr(root, "user_default_shipping_address_pk"):
            return None

        user_default_shipping_address_pk = getattr(
            root, "user_default_shipping_address_pk"
        )
        if user_default_shipping_address_pk == root.pk:
            return True
        return False

    @staticmethod
    def resolve_is_default_billing_address(root: models.Address, _info):
        """Look if the address is the default billing address of the user.

        This field is added through annotation when using the
        `resolve_addresses` resolver. It's invalid for
        `resolve_default_shipping_address` and
        `resolve_default_billing_address`
        """
        if not hasattr(root, "user_default_billing_address_pk"):
            return None

        user_default_billing_address_pk = getattr(
            root, "user_default_billing_address_pk"
        )
        if user_default_billing_address_pk == root.pk:
            return True
        return False

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        return graphene.Node.get_node_from_global_id(_info, root.id)


class AccountEvent(CountableDjangoObjectType):
    date = graphene.types.datetime.DateTime(
        description="Date when event happened at in ISO 8601 format."
    )
    type = AccountEventsEnum(description="Account event type.")
    user = graphene.Field(lambda: User, description="User who performed the action.")
    order = graphene.Field(
        "koytola.graphql.order.types.Order", description="The concerned order."
    )
    product = graphene.Field(
        "koytola.graphql.product.types.Product", description="The concerned product."
    )
    profile = graphene.Field(
        "koytola.graphql.profile.types.Company", description="The concerned company profile."
    )

    class Meta:
        description = "History log of the customer."
        model = models.AccountEvent
        interfaces = [relay.Node]
        only_fields = ["id", "parameters"]

    @staticmethod
    def resolve_user(root: models.AccountEvent, info):
        user = info.context.user
        if (
            user == root.user
            or user.has_perm(AccountPermissions.MANAGE_USERS)
            or user.has_perm(AccountPermissions.MANAGE_STAFF)
        ):
            return root.user
        raise PermissionDenied()


class UserPermission(Permission):
    source_permission_groups = graphene.List(
        graphene.NonNull("koytola.graphql.account.types.Group"),
        description="List of user permission groups which contains this permission.",
        user_id=graphene.Argument(
            graphene.ID,
            description="ID of user whose groups should be returned.",
            required=True,
        ),
        required=False,
    )

    def resolve_source_permission_groups(root: Permission, _info, user_id, **_kwargs):
        user_id = from_global_id_strict_type(user_id, only_type="User", field="pk")
        groups = auth_models.Group.objects.filter(
            user__pk=user_id, permissions__name=root.name
        )
        return groups


@key("id")
@key("email")
@key("user_id")
class User(CountableDjangoObjectType):
    addresses = graphene.List(Address, description="List of all user's addresses.")
    note = graphene.String(description="A note about the customer.")
    orders = PrefetchingConnectionField(
        "koytola.graphql.order.types.Order", description="List of user's orders."
    )
    user_permissions = graphene.List(
        UserPermission, description="List of user's permissions."
    )
    permission_groups = graphene.List(
        "koytola.graphql.account.types.Group",
        description="List of user's permission groups.",
    )
    editable_groups = graphene.List(
        "koytola.graphql.account.types.Group",
        description="List of user's permission groups which user can manage.",
    )
    avatar = graphene.Field(Image, size=graphene.Int(description="Size of the avatar."))
    events = graphene.List(
        AccountEvent, description="List of events associated with the user."
    )
    stored_payment_sources = graphene.List(
        "koytola.graphql.payment.types.PaymentSource",
        description="List of stored payment sources.",
    )
    company = graphene.Field(Company, description="Seller Company.")

    class Meta:
        description = "Represents user data."
        interfaces = [relay.Node, ObjectWithMetadata]
        model = get_user_model()
        only_fields = [
            "date_joined",
            "default_billing_address",
            "default_shipping_address",
            "email",
            "phone",
            "first_name",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "last_name",
            "note",
            "is_seller",
            "user_id",
        ]

    @staticmethod
    def resolve_addresses(root: models.User, _info, **_kwargs):
        return root.addresses.annotate_default(root).all()

    @staticmethod
    def resolve_user_permissions(root: models.User, _info, **_kwargs):
        from .resolvers import resolve_permissions

        return resolve_permissions(root)

    @staticmethod
    def resolve_permission_groups(root: models.User, _info, **_kwargs):
        return root.groups.all()

    @staticmethod
    def resolve_editable_groups(root: models.User, _info, **_kwargs):
        return get_groups_which_user_can_manage(root)

    @staticmethod
    @one_of_permissions_required(
        [AccountPermissions.MANAGE_USERS, AccountPermissions.MANAGE_STAFF]
    )
    def resolve_note(root: models.User, info):
        return root.note

    @staticmethod
    @one_of_permissions_required(
        [AccountPermissions.MANAGE_USERS, AccountPermissions.MANAGE_STAFF]
    )
    def resolve_events(root: models.User, info):
        return root.events.all()

    @staticmethod
    def resolve_orders(root: models.User, info, **_kwargs):
        viewer = info.context.user
        if viewer.has_perm(OrderPermissions.MANAGE_ORDERS):
            return root.orders.all()  # type: ignore
        return root.orders.completed()  # type: ignore

    @staticmethod
    def resolve_avatar(root: models.User, info, size=None, **_kwargs):
        if root.avatar:
            return Image.get_adjusted(
                image=root.avatar,
                alt=None,
                size=size,
                rendition_key_set="user_avatars",
                info=info,
            )

    @staticmethod
    def resolve_stored_payment_sources(root: models.User, info):
        from .resolvers import resolve_payment_sources

        if root == info.context.user:
            return resolve_payment_sources(root)
        raise PermissionDenied()

    @staticmethod
    def __resolve_reference(root, _info, **_kwargs):
        if root.id is not None:
            return graphene.Node.get_node_from_global_id(_info, root.id)
        return get_user_model().objects.get(email=root.email)

    @classmethod
    def resolve_company(cls, root, info, **data):
        user = root
        if profile_models.Company.objects.filter(user=user).exists() and user.is_seller:
            return profile_models.Company.objects.get(user=user)
        else:
            return None


class ChoiceValue(graphene.ObjectType):
    raw = graphene.String()
    verbose = graphene.String()


class AddressValidationData(graphene.ObjectType):
    country_code = graphene.String()
    country_name = graphene.String()
    address_format = graphene.String()
    address_latin_format = graphene.String()
    allowed_fields = graphene.List(graphene.String)
    required_fields = graphene.List(graphene.String)
    upper_fields = graphene.List(graphene.String)
    country_area_type = graphene.String()
    country_area_choices = graphene.List(ChoiceValue)
    city_type = graphene.String()
    city_choices = graphene.List(ChoiceValue)
    city_area_type = graphene.String()
    city_area_choices = graphene.List(ChoiceValue)
    postal_code_type = graphene.String()
    postal_code_matchers = graphene.List(graphene.String)
    postal_code_examples = graphene.List(graphene.String)
    postal_code_prefix = graphene.String()


class StaffNotificationRecipient(CountableDjangoObjectType):
    user = graphene.Field(
        User,
        description="Returns a user subscribed to email notifications.",
        required=False,
    )
    email = graphene.String(
        description=(
            "Returns email address of a user subscribed to email notifications."
        ),
        required=False,
    )
    active = graphene.Boolean(description="Determines if a notification active.")

    class Meta:
        description = (
            "Represents a recipient of email notifications send by Saleor, "
            "such as notifications about new orders. Notifications can be "
            "assigned to staff users or arbitrary email addresses."
        )
        interfaces = [relay.Node]
        model = models.StaffNotificationRecipient
        only_fields = ["user", "active"]

    @staticmethod
    def resolve_user(root: models.StaffNotificationRecipient, info):
        user = info.context.user
        if user == root.user or user.has_perm(AccountPermissions.MANAGE_STAFF):
            return root.user
        raise PermissionDenied()

    @staticmethod
    def resolve_email(root: models.StaffNotificationRecipient, _info):
        return root.get_email()


@key(fields="id")
class Group(CountableDjangoObjectType):
    users = graphene.List(User, description="List of group users")
    permissions = graphene.List(Permission, description="List of group permissions")
    user_can_manage = graphene.Boolean(
        required=True,
        description=(
            "True, if the currently authenticated user has rights to manage a group."
        ),
    )

    class Meta:
        description = "Represents permission group data."
        interfaces = [relay.Node]
        model = auth_models.Group
        only_fields = ["name", "permissions", "id"]

    @staticmethod
    @permission_required(AccountPermissions.MANAGE_STAFF)
    def resolve_users(root: auth_models.Group, _info):
        return root.user_set.all()

    @staticmethod
    def resolve_permissions(root: auth_models.Group, _info):
        permissions = root.permissions.prefetch_related("content_type").order_by(
            "codename"
        )
        return format_permissions_for_display(permissions)

    @staticmethod
    def resolve_user_can_manage(root: auth_models.Group, info):
        user = info.context.user
        return can_user_manage_group(user, root)
