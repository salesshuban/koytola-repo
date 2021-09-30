import graphene

from ...core.exceptions import PermissionDenied
from ...core.permissions import SitePermissions
from ...site.models import (
    ContactMessage,
    SiteSubscriber,
)


def resolve_contact_message(info, id=None):
    assert id, "No contact message ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([SitePermissions.MANAGE_SETTINGS]):
            _model, contact_message_pk = graphene.Node.from_global_id(id)
            return ContactMessage.objects.filter(pk=contact_message_pk).first()
    raise PermissionDenied()


def resolve_contact_messages(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([SitePermissions.MANAGE_SETTINGS]):
            return ContactMessage.objects.all().order_by("-date_submitted")
    raise PermissionDenied()


def resolve_site_subscriber(info, id=None):
    assert id, "No site subscriber ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([SitePermissions.MANAGE_SETTINGS]):
            _model, subscriber_pk = graphene.Node.from_global_id(id)
            return SiteSubscriber.objects.filter(pk=subscriber_pk).first()
    raise PermissionDenied()


def resolve_site_subscribers(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([SitePermissions.MANAGE_SETTINGS]):
            return SiteSubscriber.objects.all().order_by("-creation_date")
    raise PermissionDenied()
