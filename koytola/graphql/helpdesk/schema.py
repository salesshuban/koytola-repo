import graphene

from ..core.fields import FilterInputConnectionField
from .mutations import TicketCreate, TicketUpdate, TicketDelete
from .bulk_mutations import TicketBulkDelete, TicketBulkUpdate
from .resolvers import resolve_ticket, resolve_tickets
from .types import Ticket


class HelpdeskQueries(graphene.ObjectType):
    ticket = graphene.Field(
        Ticket,
        id=graphene.Argument(graphene.ID, description="ID of the ticket."),
        description="Look up a ticket by ID.",
    )
    tickets = FilterInputConnectionField(
        Ticket,
        description="List of user tickets.",
    )

    def resolve_ticket(self, info, id=None):
        return resolve_ticket(info, id)

    def resolve_tickets(self, info, **kwargs):
        return resolve_tickets(info, **kwargs)


class HelpdeskMutations(graphene.ObjectType):
    ticket_create = TicketCreate.Field()
    ticket_update = TicketUpdate.Field()
    ticket_delete = TicketDelete.Field()
    ticket_bulk_delete = TicketBulkDelete.Field()
    ticket_bulk_update = TicketBulkUpdate.Field()
