import graphene
from django.db.models import Q

from ...analytics.models import (
    Tracking
)
from ...core.exceptions import PermissionDenied
from ...core.permissions import AnalyticsPermissions


def resolve_tracking(info, id=None):
    assert id, "No tracking ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, url_pk = graphene.Node.from_global_id(id)
        if id is not None:
            if user.has_perms([AnalyticsPermissions.MANAGE_TRACKING]):
                return Tracking.objects.filter(pk=url_pk).first()
            else:
                url = Tracking.objects.filter(pk=url_pk).first()
                if url.user == user:
                    return url
    raise PermissionDenied()


def resolve_trackings(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([AnalyticsPermissions.MANAGE_TRACKING]):
            return Tracking.objects.all().order_by("-date")
        else:
            return Tracking.objects.filter(Q(user=user))
    raise PermissionDenied()


def resolve_user_trackings(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return Tracking.objects.filter(Q(user=user))
    raise PermissionDenied()
