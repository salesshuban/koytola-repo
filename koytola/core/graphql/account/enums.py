import graphene
from django_countries import countries

from ...account import AccountEvents
from ...account.utils import AddressType
from ...graphql.core.enums import to_enum
from ..core.utils import str_to_enum

AddressTypeEnum = to_enum(AddressType, type_name="AddressTypeEnum")
AccountEventsEnum = graphene.Enum(
    "AccountEvents", [
        (
            str_to_enum(event[0]), event[0].upper()
        ) for event in AccountEvents.CHOICES
    ]
)


CountryCodeEnum = graphene.Enum(
    "CountryCode", [(str_to_enum(country[0]), country[0]) for country in countries]
)


class AccountStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class UserType(graphene.Enum):
    SELLER = "seller"
    BUYER = "buyer"


class StaffMemberStatus(graphene.Enum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"
