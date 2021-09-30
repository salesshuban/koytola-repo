import graphene

from ...product import ProductUnits, DeliveryTimeOption
from ...graphql.core.enums import to_enum


ProductUnitsEnum = to_enum(ProductUnits, type_name="ProductUnitsEnum")
DeliveryTimeOptionEnum = to_enum(DeliveryTimeOption, type_name="DeliveryTimeOptionEnum")


class ProductStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    HIDDEN = "hidden"
    PUBLISHED = "published"


class ProductActivationStatus(graphene.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ProductPublishedStatus(graphene.Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"
