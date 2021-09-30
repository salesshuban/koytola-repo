import graphene
from django.db.models import Q

from ...core.exceptions import PermissionDenied
from ...core.permissions import OrderPermissions
from ...order import models
from ..utils.filters import filter_by_period


ORDER_SEARCH_FIELDS = ("id", "token", "user_email", "user__email")


def resolve_order(info, order_id):
    assert order_id, "No order ID provided."
    user = info.context.user
    _model, order_pk = graphene.Node.from_global_id(order_id)

    if user and not user.is_anonymous:
        if order_id is not None:
            if user.has_perms([OrderPermissions.MANAGE_ORDERS]):
                return models.Order.objects.filter(pk=order_pk).first()
            else:
                return models.Order.objects.filter(Q(user=user) & Q(pk=order_pk)).first()
        else:
            return models.Order.objects.filter(user=user).first()
    return PermissionDenied()


def resolve_orders(info, created=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([OrderPermissions.MANAGE_ORDERS]):
            qs = models.Order.objects.all().order_by("-created")
        else:
            qs = models.Order.objects.filter(user=user).order_by("-created")
        if created is not None:
            return filter_by_period(qs, created, "created")
        else:
            return qs
    return PermissionDenied()


def resolve_paid_orders(info, created=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([OrderPermissions.MANAGE_ORDERS]):
            qs = models.Order.objects.paid().order_by("-created")
        else:
            qs = models.Order.objects.paid().filter(user=user).order_by("-created")
        if created is not None:
            return filter_by_period(qs, created, "created")
        else:
            return qs
    return PermissionDenied()


def resolve_pending_orders(info, created=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([OrderPermissions.MANAGE_ORDERS]):
            qs = models.Order.objects.pending().order_by("-created")
        else:
            qs = models.Order.objects.pending().filter(user=user).order_by("-created")
        if created is not None:
            return filter_by_period(qs, created, "created")
        else:
            return qs
    return PermissionDenied()


def resolve_cancelled_orders(info, created=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([OrderPermissions.MANAGE_ORDERS]):
            qs = models.Order.objects.cancelled().order_by("-created")
        else:
            qs = models.Order.objects.cancelled().filter(user=user).order_by("-created")
        if created is not None:
            return filter_by_period(qs, created, "created")
        else:
            return qs
    return PermissionDenied()


def resolve_order_by_token(token):
    return models.Order.objects.filter(token=token).first()
