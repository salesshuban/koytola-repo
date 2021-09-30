from typing import Any, List

from ...account import models as account_models
from ...core.exceptions import PermissionDenied
from ...core.permissions import (
    AccountPermissions,
    AppPermission,
    BasePermissionEnum,
    OrderPermissions,
)


def no_permissions(_info, _object_pk: Any) -> List[None]:
    return []


def public_user_permissions(info, user_pk: int) -> List[BasePermissionEnum]:
    """Resolve permission for access to public metadata for user.

    Customer have access to own public metadata.
    """
    user = account_models.User.objects.filter(pk=user_pk).first()
    if not user:
        raise PermissionDenied()
    if info.context.user.pk == user.pk:
        return []
    return [AccountPermissions.MANAGE_USERS]


def private_user_permissions(_info, user_pk: int) -> List[BasePermissionEnum]:
    user = account_models.User.objects.filter(pk=user_pk).first()
    if not user:
        raise PermissionDenied()
    return [AccountPermissions.MANAGE_USERS]


def order_permissions(_info, _object_pk: Any) -> List[BasePermissionEnum]:
    return [OrderPermissions.MANAGE_ORDERS]


def invoice_permissions(_info, _object_pk: Any) -> List[BasePermissionEnum]:
    return [OrderPermissions.MANAGE_ORDERS]


def app_permissions(_info, _object_pk: int) -> List[BasePermissionEnum]:
    return [AppPermission.MANAGE_APPS]


PUBLIC_META_PERMISSION_MAP = {
    "Order": no_permissions,
    "Invoice": invoice_permissions,
    "App": app_permissions,
    "User": public_user_permissions,
}


PRIVATE_META_PERMISSION_MAP = {
    "Order": order_permissions,
    "Invoice": invoice_permissions,
    "App": app_permissions,
    "User": private_user_permissions,
}
