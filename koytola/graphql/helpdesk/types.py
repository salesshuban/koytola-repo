from graphene import relay

from ...helpdesk import models
from ..core.connection import CountableDjangoObjectType


class Ticket(CountableDjangoObjectType):

    class Meta:
        description = (
            "User helpdesk ticket."
        )
        only_fields = [
            "id",
            "user",
            "type",
            "subject",
            "content",
            "creation_date",
            "notes",
            "status",
            "update_date",
        ]
        interfaces = [relay.Node]
        model = models.Ticket
