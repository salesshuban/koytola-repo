import graphene

from ..core.types import SortInputObjectType


class ProductSortField(graphene.Enum):
    SLUG = ["slug", "pk"]
    NAME = ["name", "pk"]
    HSCODE = ["hs_code", "pk"]
    CATEGORY = ["category", "pk"]
    UNITPRICE = ["unit_price", "pk"]
    BRAND = ["brand", "pk"]
    MOQ = ["minimum_order_quantity", "pk"]
    DATE_CREATED = ["creation_date", "pk"]
    IS_PUBLISHED = ["is_published", "pk"]


    @property
    def description(self):
        if self.name in ProductSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort products by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ProductSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = ProductSortField
        type_name = "products"


class OfferSortField(graphene.Enum):
    TITLE = ["title", "pk"]
    SLUG = ["slug", "pk"]
    GETCODE = ["get_code", "pk"]
    UNIT = ["unit", "pk"]
    VALUE = ["value", "pk"]
    STARTDATE = ["start_date", "pk"]
    ENDDATE = ["end_date", "pk"]
    TAGS = ["tags", "pk"]
    ISACTIVE = ["is_active", "pk"]


class ProductQuerySortField(graphene.Enum):
    USER = ["user", "pk"]
    PRODUCT = ["product", "pk"]
    QUANTITY = ["quantity", "pk"]
    ISCLOSED = ["is_closed", "pk"]


class PortDealsSortingSortField(graphene.Enum):
    NAME = ["name", "pk"]
    SLUG = ["slug", "pk"]
    PRODUCT = ["product_name", "pk"]
    UNIT = ["unit", "pk"]
    QUANTITY = ["quantity", "pk"]
    STARTDATE = ["start_date", "pk"]
    ENDDATE = ["end_date", "pk"]
    PRICE = ["price", "pk"]


class OfferSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = OfferSortField
        type_name = "products"


class ProductQuerySortingInput(SortInputObjectType):
    class Meta:
        sort_enum = ProductQuerySortField
        type_name = "products"


class PortDealsSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = PortDealsSortingSortField
        type_name = "port_deals"
