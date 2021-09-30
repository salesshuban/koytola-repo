import graphene
from django.core.exceptions import ValidationError

from ..account.types import User
from ...core.permissions import HelpdeskPermissions
from ...core.exceptions import PermissionDenied
from ...helpdesk import models
from ...helpdesk.error_codes import HelpdeskErrorCode
from ..helpdesk.types import Ticket
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types.common import HelpdeskError


def clean_ticket(info, ticket):
    # Raise error if the current user doesn't have permission.
    if ticket.user and ticket.user != info.context.user:
        if not info.context.user.has_perm(HelpdeskPermissions.MANAGE_TICKETS):
            raise PermissionDenied()

    # Raise error if the ticket status is completed.
    if ticket.status == "Completed":
        if not info.context.user.has_perm(HelpdeskPermissions.MANAGE_TICKETS):
            raise PermissionDenied()


class TicketInput(graphene.InputObjectType):
    type = graphene.String(description="Ticket type.")
    subject = graphene.String(description="Ticket subject.")
    content = graphene.String(description="Ticket content.")
    note = graphene.String(description="Ticket notes.")
    status = graphene.String(description="Ticket status.")


class TicketCreate(ModelMutation):
    ticket = graphene.Field(Ticket, description="A created ticket.")

    class Arguments:
        input = TicketInput(
            required=True, description="Fields required to create a ticket."
        )

    class Meta:
        description = "Creates a new ticket."
        model = models.Ticket
        return_field_name = "ticket"
        error_type_class = HelpdeskError
        error_type_field = "helpdesk_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        return cleaned_input

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        instance.user = info.context.user
        return instance

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()


class TicketUpdate(ModelMutation):
    ticket = graphene.Field(Ticket, description="An updated ticket.")

    class Arguments:
        ticket_id = graphene.ID(required=True, description="ID of a ticket to update.")
        input = TicketInput(
            required=True, description="Fields required to update a ticket."
        )

    class Meta:
        description = "Updates an existing ticket."
        model = models.Ticket
        error_type_class = HelpdeskError
        error_type_field = "helpdesk_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, ticket_id, **data):
        ticket = cls.get_node_or_error(
            info, ticket_id, only_type=Ticket, field="ticket_id"
        )
        clean_ticket(info, ticket)
        cleaned_input = cls.clean_input(info, ticket, data.get("input"))
        ticket = cls.construct_instance(ticket, cleaned_input)
        cls.clean_instance(info, ticket)
        cls.save(info, ticket, cleaned_input)
        return TicketUpdate(ticket=ticket)


class TicketDelete(ModelDeleteMutation):
    class Arguments:
        ticket_id = graphene.ID(required=True, description="ID of a ticket to delete.")

    class Meta:
        description = "Deletes a ticket."
        model = models.Ticket
        error_type_class = HelpdeskError
        error_type_field = "helpdesk_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, ticket_id, **data):
        ticket = cls.get_node_or_error(
            info, ticket_id, only_type=Ticket, field="ticket_id"
        )
        clean_ticket(info, ticket)
        ticket.delete()
        return TicketDelete(ticket=ticket)
