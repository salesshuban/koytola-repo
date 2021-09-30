import graphene

from ....core.permissions import AccountPermissions
from ....account import models
from ...core.mutations import ModelDeleteMutation
from ...core.types.common import AccountError
from ..types import AccountEvent
from ..utils import account_event_permission


class AccountEventDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of an account event to delete.")

    class Meta:
        description = "Deletes an account event."
        model = models.AccountEvent
        permissions = (AccountPermissions.MANAGE_ACCOUNT_EVENTS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        model_type = cls.get_type_for_model()
        event = cls.get_node_or_error(
            info, id, only_type=model_type, field="id"
        )
        account_event_permission(info, event)
        event.delete()
        return AccountEventDelete(event=event)

    @classmethod
    def get_type_for_model(cls):
        return AccountEvent
