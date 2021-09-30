from collections import defaultdict

import graphene
from django.core.exceptions import ValidationError

from ...account import models
from ...account.error_codes import AccountErrorCode
from ...core.permissions import AccountPermissions
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation
from ..core.types.common import AccountError, StaffError
from ..core.utils import list_to_queryset
from .types import User, AccountEvent
from .utils import (
    AccountDeleteMixin,
    StaffDeleteMixin,
    account_event_bulk_permission
)


class UserBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of user IDs to delete."
        )

    class Meta:
        abstract = True


class AccountBulkDelete(AccountDeleteMixin, UserBulkDelete):
    class Meta:
        description = "Deletes accounts."
        model = models.User
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        count, errors = super().perform_mutation(root, info, **data)
        cls.post_process(info, count)
        return count, errors


class StaffBulkDelete(StaffDeleteMixin, UserBulkDelete):
    class Meta:
        description = "Deletes staff users."
        model = models.User
        permissions = (AccountPermissions.MANAGE_STAFF,)
        error_type_class = StaffError
        error_type_field = "staff_errors"

    @classmethod
    def perform_mutation(cls, _root, info, ids, **data):
        instances = cls.get_nodes_or_error(ids, "id", User)
        errors = cls.clean_instances(info, instances)
        count = len(instances)
        if not errors and count:
            clean_instance_ids = [instance.pk for instance in instances]
            qs = models.User.objects.filter(pk__in=clean_instance_ids)
            cls.bulk_action(queryset=qs, **data)
        else:
            count = 0
        return count, errors

    @classmethod
    def clean_instances(cls, info, users):
        errors = defaultdict(list)
        requestor = info.context.user
        cls.check_if_users_can_be_deleted(info, users, "ids", errors)
        cls.check_if_requestor_can_manage_users(requestor, users, "ids", errors)
        cls.check_if_removing_left_not_manageable_permissions(
            requestor, users, "ids", errors
        )
        return ValidationError(errors) if errors else {}


class UserBulkSetActive(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of user IDs to (de)activate)."
        )
        is_active = graphene.Boolean(
            required=True, description="Determine if users will be set active or not."
        )

    class Meta:
        description = "Activate or deactivate users."
        model = models.User
        permissions = (AccountPermissions.MANAGE_USERS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def clean_instance(cls, info, instance):
        if info.context.user == instance:
            raise ValidationError(
                {
                    "is_active": ValidationError(
                        "Cannot activate or deactivate your own account.",
                        code=AccountErrorCode.ACTIVATE_OWN_ACCOUNT,
                    )
                }
            )
        elif instance.is_superuser:
            raise ValidationError(
                {
                    "is_active": ValidationError(
                        "Cannot activate or deactivate superuser's account.",
                        code=AccountErrorCode.ACTIVATE_SUPERUSER_ACCOUNT,
                    )
                }
            )

    @classmethod
    def bulk_action(cls, queryset, is_active):
        queryset.update(is_active=is_active)


class AccountEventBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of account event IDs to delete."
        )

    class Meta:
        description = "Deletes account events."
        model = models.AccountEvent
        permissions = (AccountPermissions.MANAGE_ACCOUNT_EVENTS,)
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def perform_mutation(cls, root, info, ids, **data):
        errors = {}
        if not ids:
            return 0, errors
        model_type = cls.get_type_for_model()
        events = cls.get_nodes_or_error(
            ids, only_type=model_type, field="id"
        )
        account_event_bulk_permission(info, events)
        queryset = list_to_queryset(events)
        cls.bulk_action(queryset)
        return len(events), errors

    @classmethod
    def bulk_action(cls, queryset):
        queryset.delete()

    @classmethod
    def get_type_for_model(cls):
        return AccountEvent
