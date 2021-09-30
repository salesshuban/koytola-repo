from typing import Optional

from ..order.models import Order
from . import AccountEvents
from .models import AccountEvent, User


def account_created_event(*, user: User) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(user=user, type=AccountEvents.ACCOUNT_CREATED)


def account_deleted_event(*, user: User) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(user=user, type=AccountEvents.ACCOUNT_DELETED)


def account_password_reset_link_sent_event(*, user_id: int) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(
        user_id=user_id, type=AccountEvents.PASSWORD_RESET_LINK_SENT
    )


def account_password_reset_event(*, user: User) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(user=user, type=AccountEvents.PASSWORD_RESET)


def account_password_changed_event(*, user: User) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(user=user, type=AccountEvents.PASSWORD_CHANGED)


def account_email_change_request_event(
    *, user_id: int, parameters: dict
) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(
        user_id=user_id, type=AccountEvents.EMAIL_CHANGE_REQUEST, parameters=parameters
    )


def account_email_changed_event(
    *, user: User, parameters: dict
) -> Optional[AccountEvent]:
    return AccountEvent.objects.create(
        user=user, type=AccountEvents.EMAIL_CHANGED, parameters=parameters
    )


def account_order_event(*, user: User, order: Order) -> Optional[AccountEvent]:
    if user.is_anonymous:
        return None

    return AccountEvent.objects.create(
        user=user, order=order, type=AccountEvents.ORDER_UPDATE
    )


def account_added_to_note_order_event(
    *, user: User, order: Order, message: str
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=user,
        order=order,
        type=AccountEvents.NOTE_ADDED_TO_ORDER,
        parameters={"message": message},
    )


def staff_user_added_to_note_order_event(
    *, staff_user: User, order: Order, message: str
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=staff_user,
        order=order,
        type=AccountEvents.NOTE_ADDED_TO_ORDER_BY_STAFF,
        parameters={"message": message},
    )


def staff_user_deleted_an_account_event(
    *, staff_user: User, deleted_count: int = 1
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=staff_user,
        order=None,
        type=AccountEvents.ACCOUNT_DELETED_BY_STAFF,
        parameters={"count": deleted_count},
    )


def staff_user_assigned_email_to_an_account_event(
    *, staff_user: User, new_email: str
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=staff_user,
        order=None,
        type=AccountEvents.EMAIL_ASSIGNED_BY_STAFF,
        parameters={"message": new_email},
    )


def staff_user_added_note_to_an_account_event(
    *, staff_user: User, note: str
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=staff_user,
        order=None,
        type=AccountEvents.NOTE_ADDED_BY_STAFF,
        parameters={"message": note},
    )


def staff_user_assigned_name_to_an_account_event(
    *, staff_user: User, new_name: str
) -> AccountEvent:
    return AccountEvent.objects.create(
        user=staff_user,
        order=None,
        type=AccountEvents.NAME_ASSIGNED_BY_STAFF,
        parameters={"message": new_name},
    )
