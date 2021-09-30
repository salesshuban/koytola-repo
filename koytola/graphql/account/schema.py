import graphene
import csv
from ...core.permissions import AccountPermissions
from ..core.fields import FilterInputConnectionField
from ..core.types import FilterInputObjectType
from ..decorators import permission_required
from .bulk_mutations import (
    AccountBulkDelete,
    StaffBulkDelete,
    UserBulkSetActive,
    AccountEventBulkDelete,
)
from .enums import CountryCodeEnum
from .filters import (
    AccountFilter,
    PermissionGroupFilter,
    StaffUserFilter,
    EventFilter,
)
from .mutations.account import (
    AccountAddressCreate,
    AccountAddressDelete,
    AccountAddressUpdate,
    AccountDelete,
    AccountDeletebyRequest,
    AccountUpdate,
    AccountRegister,
    AccountRequestDeletion,
    AccountSetDefaultAddress,
    ConfirmEmailChange,
    RequestEmailChange,
)
from .mutations.base import (
    ConfirmAccount,
    PasswordChange,
    RequestPasswordReset,
    SetPassword,
    ForgotPasswordEmailSend
)
from .mutations.event import (
    AccountEventDelete,
)
from .mutations.jwt import (
    CreateToken,
    DeactivateAllUserTokens,
    RefreshToken,
    VerifyToken,
)
from .mutations.permission_group import (
    PermissionGroupCreate,
    PermissionGroupDelete,
    PermissionGroupUpdate,
)
from .mutations.staff import (
    models,
    AddressCreate,
    AddressDelete,
    AddressSetDefault,
    AddressUpdate,
    AccountCreatebyStaff,
    AccountDeletebyStaff,
    AccountUpdatebyStaff,
    StaffCreate,
    StaffDelete,
    StaffUpdate,
    UserAvatarDelete,
    UserAvatarUpdate,
)
from .resolvers import (
    resolve_address,
    resolve_address_validation_rules,
    resolve_accounts,
    resolve_users,
    resolve_permission_groups,
    resolve_staff_users,
    resolve_user,
    resolve_account_events,
    resolve_countries
)
from .sorters import (
    PermissionGroupSortingInput,
    UserSortingInput,
    EventSortingInput,
)
from .types import (
    AccountEvent,
    Address,
    AddressValidationData,
    Group,
    User,
    Countries
)


class AccountFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = AccountFilter


class PermissionGroupFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = PermissionGroupFilter


class StaffUserInput(FilterInputObjectType):
    class Meta:
        filterset_class = StaffUserFilter


class EventFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = EventFilter


class AccountQueries(graphene.ObjectType):
    address_validation_rules = graphene.Field(
        AddressValidationData,
        description="Returns address validation rules.",
        country_code=graphene.Argument(
            CountryCodeEnum,
            description="Two-letter ISO 3166-1 country code.",
            required=True,
        ),
        country_area=graphene.Argument(
            graphene.String, description="Designation of a region, province or state."
        ),
        city=graphene.Argument(graphene.String, description="City or a town name."),
        city_area=graphene.Argument(
            graphene.String, description="Sublocality like a district."
        ),
    )
    address = graphene.Field(
        Address,
        id=graphene.Argument(
            graphene.ID, description="ID of an address.", required=True
        ),
        description="Look up an address by ID.",
    )
    accounts = FilterInputConnectionField(
        User,
        filter=AccountFilterInput(description="Filtering options for accounts."),
        sort_by=UserSortingInput(description="Sort accounts."),
        description="List of the shop's accounts.",
    )
    countries = graphene.List(
        Countries,
        description="List of the shop's accounts.",
    )
    permission_groups = FilterInputConnectionField(
        Group,
        filter=PermissionGroupFilterInput(
            description="Filtering options for permission groups."
        ),
        sort_by=PermissionGroupSortingInput(description="Sort permission groups."),
        description="List of permission groups.",
    )
    permission_group = graphene.Field(
        Group,
        id=graphene.Argument(
            graphene.ID, description="ID of the group.", required=True
        ),
        description="Look up permission group by ID.",
    )
    me = graphene.Field(User, description="Return the currently authenticated user.")
    staff_users = FilterInputConnectionField(
        User,
        filter=StaffUserInput(description="Filtering options for staff users."),
        sort_by=UserSortingInput(description="Sort staff users."),
        description="List of the shop's staff users.",
    )

    user = graphene.Field(
        User,
        id=graphene.Argument(graphene.ID, description="ID of the user.", required=False),
        description="Look up a user by ID.",
    )
    users = FilterInputConnectionField(
        User,
        filter=AccountFilterInput(description="Filtering options for accounts."),
        sort_by=UserSortingInput(description="Sort all accounts."),
        description="List of the all accounts.",
    )
    account_events = FilterInputConnectionField(
        AccountEvent,
        filter=EventFilterInput(description="Filtering account events."),
        sort_by=EventSortingInput(description="Sort account events."),
        description="List of the account events.",
    )
    staff_events = FilterInputConnectionField(
        AccountEvent,
        filter=EventFilterInput(description="Filtering staff events."),
        sort_by=EventSortingInput(description="Sort staff events."),
        description="List of the staff member events.",
    )

    def resolve_address_validation_rules(self, info, country_code, country_area=None, city=None, city_area=None):
        return resolve_address_validation_rules(
            info,
            country_code,
            country_area=country_area,
            city=city,
            city_area=city_area,
        )

    @permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_accounts(self, info, query=None, **kwargs):
        return resolve_accounts(info, query=query, **kwargs)
    
    def resolve_countries(self, info, **kwargs):
        return resolve_countries(info, **kwargs)

    @permission_required(AccountPermissions.MANAGE_STAFF)
    def resolve_permission_groups(self, info, query=None, **kwargs):
        return resolve_permission_groups(info, query=query, **kwargs)

    @permission_required(AccountPermissions.MANAGE_STAFF)
    def resolve_permission_group(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, Group)

    def resolve_me(self, info):
        user = info.context.user
        return user if user.is_authenticated else None

    @permission_required(AccountPermissions.MANAGE_STAFF)
    def resolve_staff_users(self, info, query=None, **kwargs):
        return resolve_staff_users(info, query=query, **kwargs)

    def resolve_user(self, info, id=None):
        return resolve_user(info, id)

    @permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_users(self, info, query=None, **kwargs):
        return resolve_users(info, query=query, **kwargs)

    def resolve_address(self, info, id):
        return resolve_address(info, id)

    @permission_required(AccountPermissions.MANAGE_USERS)
    def resolve_account_events(self, info, id=None, **kwargs):
        return resolve_account_events(info, id, **kwargs)


class AccountMutations(graphene.ObjectType):
    # Base mutations
    token_create = CreateToken.Field()
    token_refresh = RefreshToken.Field()
    token_verify = VerifyToken.Field()
    tokens_deactivate_all = DeactivateAllUserTokens.Field()

    request_password_reset = RequestPasswordReset.Field()
    confirm_account = ConfirmAccount.Field()
    set_password = SetPassword.Field()
    password_change = PasswordChange.Field()
    forgot_password_email_send = ForgotPasswordEmailSend.Field()
    request_email_change = RequestEmailChange.Field()
    confirm_email_change = ConfirmEmailChange.Field()

    # Account mutations
    account_address_create = AccountAddressCreate.Field()
    account_address_update = AccountAddressUpdate.Field()
    account_address_delete = AccountAddressDelete.Field()
    account_set_default_address = AccountSetDefaultAddress.Field()

    account_register = AccountRegister.Field()
    account_update = AccountUpdate.Field()
    account_request_deletion = AccountRequestDeletion.Field()
    account_delete = AccountDelete.Field()
    account_delete_by_request = AccountDeletebyRequest.Field()

    # Event mutations
    account_event_delete = AccountEventDelete.Field()
    account_event_bulk_delete = AccountEventBulkDelete.Field()

    # Staff mutations
    address_create = AddressCreate.Field()
    address_update = AddressUpdate.Field()
    address_delete = AddressDelete.Field()
    address_set_default = AddressSetDefault.Field()

    account_create_by_staff = AccountCreatebyStaff.Field()
    account_update_by_staff = AccountUpdatebyStaff.Field()
    account_delete_by_staff = AccountDeletebyStaff.Field()
    account_bulk_delete = AccountBulkDelete.Field()

    staff_create = StaffCreate.Field()
    staff_update = StaffUpdate.Field()
    staff_delete = StaffDelete.Field()
    staff_bulk_delete = StaffBulkDelete.Field()

    user_avatar_update = UserAvatarUpdate.Field()
    user_avatar_delete = UserAvatarDelete.Field()
    user_bulk_set_active = UserBulkSetActive.Field()

    # Permission group mutations
    permission_group_create = PermissionGroupCreate.Field()
    permission_group_update = PermissionGroupUpdate.Field()
    permission_group_delete = PermissionGroupDelete.Field()
