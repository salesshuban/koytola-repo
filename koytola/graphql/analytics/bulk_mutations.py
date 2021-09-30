import graphene

from ...analytics import models
from ...core.permissions import AnalyticsPermissions
from ..core.mutations import ModelBulkDeleteMutation
from ..core.types.common import AnalyticsError


class TrackingBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of tracking to delete."
        )

    class Meta:
        description = "Deletes tracking"
        model = models.Tracking
        permissions = (AnalyticsPermissions.MANAGE_TRACKING,)
        error_type_class = AnalyticsError
        error_type_field = "analytics_errors"

    @classmethod
    def bulk_action(cls, queryset):
        queryset.delete()
