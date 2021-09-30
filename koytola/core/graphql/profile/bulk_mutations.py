import graphene

from ...core.permissions import ProfilePermissions
from ...profile.models import Company
from ..core.mutations import ModelBulkDeleteMutation, BaseBulkMutation
from ..core.types.common import ProfileError


class CompanyBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company profiles to delete."
        )

    class Meta:
        description = "Deletes company profiles."
        model = Company
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"


class CompanyBulkUpdate(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company profiles to update."
        )
        is_active = graphene.Boolean(
            required=True, description="Update the status of company profiles."
        )

    class Meta:
        description = "Updates company profiles."
        model = Company
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def bulk_action(cls, queryset, is_active):
        queryset.update(is_active=is_active)
