import graphene

from ...core.permissions import AnalyticsPermissions
from ..core.fields import FilterInputConnectionField
from ..decorators import permission_required
from .bulk_mutations import TrackingBulkDelete
from .filters import (
    TrackingFilterInput,
    UserTrackingFilterInput
)
from .mutations import TrackingDelete, TrackingUpdate
from .resolvers import (
    resolve_tracking,
    resolve_trackings,
    resolve_user_trackings,
)
from .sorters import (
    TrackingSortingInput,
    UserTrackingSortingInput,
)
from .types import (
    Tracking,
    UserTracking,
)


class AnalyticsQueries(graphene.ObjectType):
    tracking = graphene.Field(
        Tracking,
        id=graphene.Argument(
            graphene.ID, description="ID of the tracking analytics."
        ),
        description="Tracking analytics by ID.",
    )
    trackings = FilterInputConnectionField(
        Tracking,
        filter=TrackingFilterInput(
            description="Filtering options for tracking analytics."
        ),
        sort_by=TrackingSortingInput(description="Sort tracking analytics."),
        description="List of tracking analytics.",
    )
    user_trackings = FilterInputConnectionField(
        UserTracking,
        filter=UserTrackingFilterInput(
            description="Filtering options for user tracking analytics."
        ),
        sort_by=UserTrackingSortingInput(description="Sort user tracking analytics."),
        description="List of user tracking analytics.",
    )

    @permission_required(AnalyticsPermissions.MANAGE_TRACKING)
    def resolve_tracking(self, info, id=None):
        return resolve_tracking(info, id)

    @permission_required(AnalyticsPermissions.MANAGE_TRACKING)
    def resolve_trackings(self, info, **kwargs):
        return resolve_trackings(info, **kwargs)

    def resolve_user_trackings(self, info, **kwargs):
        return resolve_user_trackings(info, **kwargs)


class AnalyticsMutations(graphene.ObjectType):
    tracking_bulk_delete = TrackingBulkDelete.Field()
    tracking_delete = TrackingDelete.Field()
    tracking_update = TrackingUpdate.Field()
