import graphene

from ...graphql.core.enums import to_enum
from ...site import AuthenticationBackends, ContactMessageStatus
from ..core.utils import str_to_enum

AuthorizationKeyType = graphene.Enum(
    "AuthorizationKeyType",
    [
        (str_to_enum(auth_type[0]), auth_type[0])
        for auth_type in AuthenticationBackends.BACKENDS
    ],
)

ContactMessageStatusEnum = to_enum(ContactMessageStatus)


class SiteSubscriptionStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
