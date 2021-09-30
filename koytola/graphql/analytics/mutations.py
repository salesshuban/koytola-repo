from django.core.exceptions import ValidationError
import graphene

from ...account import models as account_models
from ...analytics import models
from ...analytics.error_codes import TrackingErrorCode
from ...core.permissions import AnalyticsPermissions
from ...product import models as product_models
from ...profile import models as profile_models
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types.common import AnalyticsError
from .types import Tracking
from .utils import validate_tracking_instance
from .enums import TrackingTypeEnum


class TrackingInput(graphene.InputObjectType):
    user = graphene.ID(
        description="Category to which item points.",
        name="user"
    )
    type = TrackingTypeEnum(description="Tracking type.", required=False)
    category = graphene.ID(
        description="Category which tracking is on.",
        name="category"
    )
    company = graphene.ID(
        description="Company which tracking is on.",
        name="company"
    )
    product = graphene.ID(
        description="Product which tracking is on.",
        name="product"
    )

    ip = graphene.String(description="IP of the Tracking.")
    country = graphene.String(description="Country of the Tracking.")
    region = graphene.String(description="Region of the Tracking.")
    city = graphene.String(description="City of the Tracking.")
    postal = graphene.String(description="Postal code of the Tracking.")
    location_details = graphene.JSONString(
        description="Location details in JSON format."
    )
    referrer = graphene.String(description="City of the Tracking.")
    device_type = graphene.String(description="City of the Tracking.")
    device = graphene.String(description="City of the Tracking.")
    browser = graphene.String(description="City of the Tracking.")
    browser_version = graphene.String(description="City of the Tracking.")
    system = graphene.String(description="City of the Tracking.")
    system_version = graphene.String(description="City of the Tracking.")

    parameters = graphene.JSONString(
        description="Other tracking parameters in JSON format."
    )


class TrackingUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a tracking to update.")
        input = TrackingInput(
            required=True, description="Fields required to update a tracking instance."
        )

    class Meta:
        description = "Updates a Tracking."
        model = models.Tracking
        permissions = (AnalyticsPermissions.MANAGE_TRACKING,)
        error_type_class = AnalyticsError
        error_type_field = "analytics_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)

        validate_tracking_instance(cleaned_input, "user", account_models.User)
        validate_tracking_instance(cleaned_input, "category", product_models.Category)
        validate_tracking_instance(cleaned_input, "company", profile_models.Company)
        validate_tracking_instance(cleaned_input, "product", product_models.Product)

        items = [
            cleaned_input.get("category"),
            cleaned_input.get("company"),
            cleaned_input.get("product"),
        ]
        items = [item for item in items if item is not None]
        if len(items) > 1:
            raise ValidationError(
                "More than one item provided.", code=TrackingErrorCode.TOO_MANY_ITEMS
            )
        return cleaned_input

    @classmethod
    def construct_instance(cls, instance, cleaned_data):
        # Only one item can be assigned per tracking
        instance.category = None
        instance.company = None
        instance.product = None
        instance.url = None
        return super().construct_instance(instance, cleaned_data)

    @classmethod
    def get_type_for_model(cls):
        return Tracking


class TrackingDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a Tracking to delete."
        )

    class Meta:
        description = "Deletes a Tracking."
        model = models.Tracking
        permissions = (AnalyticsPermissions.MANAGE_TRACKING,)
        error_type_class = AnalyticsError
        error_type_field = "analytics_errors"

    @classmethod
    def get_type_for_model(cls):
        return Tracking
