import graphene

from ...core.permissions import SitePermissions
from ...site import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation
from ..core.types.common import SiteError
from .enums import ContactMessageStatusEnum
from .types import ContactMessage, SiteSubscriber


class ContactMessageBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID,
            description="List of contact message IDs to delete.",
            required=True,
        )

    class Meta:
        description = "Delete contact messages."
        model = models.ContactMessage
        permissions = (SitePermissions.MANAGE_CONTACT_MESSAGES,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return ContactMessage


class ContactMessageBulkUpdate(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID,
            description="List of message IDs to update",
            required=True,
        )
        status = ContactMessageStatusEnum(
            description="Contact message status.",
            required=True
        )

    class Meta:
        description = "Contact messages status update."
        model = models.ContactMessage
        permissions = (SitePermissions.MANAGE_CONTACT_MESSAGES,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def bulk_action(cls, queryset, status):
        queryset.update(status=status)

    @classmethod
    def get_type_for_model(cls):
        return ContactMessage


class SiteSubscriberBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID,
            description="List of site subscriber IDs to delete.",
            required=True,
        )

    class Meta:
        description = "Delete site subscribers."
        model = models.SiteSubscriber
        permissions = (SitePermissions.MANAGE_SITE_SUBSCRIBERS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return SiteSubscriber


class SiteSubscriberBulkUpdate(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID,
            description="List of site subscriber IDs to update",
            required=True,
        )
        is_active = graphene.Boolean(
            description="Site subscriber status.",
            required=True
        )

    class Meta:
        description = "Site subscriber status update."
        model = models.SiteSubscriber
        permissions = (SitePermissions.MANAGE_SITE_SUBSCRIBERS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def bulk_action(cls, queryset, is_active):
        queryset.update(is_active=is_active)

    @classmethod
    def get_type_for_model(cls):
        return SiteSubscriber
