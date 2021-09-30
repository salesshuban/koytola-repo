import graphene

from ...profile import MessageStatus, MessageType
from ...graphql.core.enums import to_enum


MessageTypeEnum = to_enum(MessageType, type_name="MessageTypeEnum")
MessageStatusEnum = to_enum(MessageStatus, type_name="MessageStatusEnum")


class ProfileStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    HIDDEN = "hidden"
    PUBLISHED = "published"


class ProfileActivationStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProfilePublishedStatus(graphene.Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"


class ProfileCompanyType(graphene.Enum):
    MANUFACTURER = "manufacturer"
    SUPPLIER = "supplier"


class RosetterType(graphene.Enum):
    COMPANY = "Company"
    PRODUCT = "Product"
