import graphene
from graphene_federation import key

from ...analytics import models
from ..core.connection import CountableDjangoObjectType
from .dataloaders import (
    CategoryByIdLoader,
    CompanyByIdLoader,
    ProductByIdLoader,
    UserByIdLoader,
)
from .enums import TrackingTypeEnum


@key("id")
class Tracking(CountableDjangoObjectType):
    type = TrackingTypeEnum(description="Tracking analytics type.")
    user = graphene.Field(
        "koytola.graphql.account.types.User",
        description=(
            "User that tracking belongs to.",
        ),
    )
    category = graphene.Field(
        "koytola.graphql.product.types.Category",
        description=(
            "Category that Tracking belongs to",
        ),
    )
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that Tracking belongs to",
        ),
    )
    product = graphene.Field(
        "koytola.graphql.product.types.Product",
        description=(
            "Product that Tracking belongs to",
        ),
    )

    class Meta:
        description = (
            "Tracking data instance."
        )
        only_fields = [
            "id",
            "date",
            "ip",
            "country",
            "region",
            "city",
            "postal",
            "location_details",
            "referrer",
            "device_type",
            "device",
            "browser",
            "browser_version",
            "system",
            "system_version",
            "parameters",
        ]
        interfaces = [graphene.relay.Node]
        model = models.Tracking

    @staticmethod
    def resolve_user(root: models.Tracking, info, **_kwargs):
        if root.user_id:
            return UserByIdLoader(info.context).load(root.user_id)
        return None

    @staticmethod
    def resolve_category(root: models.Tracking, info, **_kwargs):
        if root.category_id:
            return CategoryByIdLoader(info.context).load(root.category_id)
        return None

    @staticmethod
    def resolve_company(root: models.Tracking, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None

    @staticmethod
    def resolve_product(root: models.Tracking, info, **_kwargs):
        if root.product_id:
            return ProductByIdLoader(info.context).load(root.product_id)
        return None


class UserTracking(CountableDjangoObjectType):
    type = TrackingTypeEnum(description="Tracking analytics type.")

    class Meta:
        description = (
            "User Tracking data instance."
        )
        only_fields = [
            "id",
            "date",
            "country",
        ]
        interfaces = [graphene.relay.Node]
        model = models.Tracking
