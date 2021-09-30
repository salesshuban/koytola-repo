import graphene

from ...core.permissions import HelpdeskPermissions
from ...helpdesk import models
from ..core.mutations import ModelBulkDeleteMutation, BaseBulkMutation
from ..core.types.common import HelpdeskError


class TicketBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of ticket IDs to delete."
        )

    class Meta:
        description = "Deletes tickets."
        model = models.Ticket
        permissions = (HelpdeskPermissions.MANAGE_TICKETS,)
        error_type_class = HelpdeskError
        error_type_field = "helpdesk_errors"


class TicketBulkUpdate(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of ticket IDs to delete."
        )
        status = graphene.String(
            required=True, description="Update the status of tickets."
        )

    class Meta:
        description = "Updates tickets."
        model = models.Ticket
        permissions = (HelpdeskPermissions.MANAGE_TICKETS,)
        error_type_class = HelpdeskError
        error_type_field = "helpdesk_errors"

    @classmethod
    def bulk_action(cls, queryset, status):
        queryset.update(status=status)
