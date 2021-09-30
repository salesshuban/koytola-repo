import graphene
from django.db.models import Q

from ...helpdesk import models
from ...core.exceptions import PermissionDenied
from ...core.permissions import HelpdeskPermissions


def resolve_ticket(info, ticket_id=None):
    assert ticket_id, "No ticket ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, ticket_pk = graphene.Node.from_global_id(ticket_id)
        if ticket_id is not None:
            if user.has_perms([HelpdeskPermissions.MANAGE_TICKETS]):
                return models.Ticket.objects.filter(pk=ticket_pk).first()
            else:
                return models.Ticket.objects.filter(Q(user=user) & Q(pk=ticket_pk)).first()
        else:
            return models.Ticket.objects.filter(user=user).first()
    return PermissionDenied()


def resolve_tickets(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([HelpdeskPermissions.MANAGE_TICKETS]):
            return models.Ticket.objects.all().order_by("-creation_date")
        else:
            return models.Ticket.objects.filter(user=user).order_by("-creation_date")
    return PermissionDenied()
