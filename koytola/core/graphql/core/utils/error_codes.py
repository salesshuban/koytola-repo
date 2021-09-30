from enum import Enum

from ....account.error_codes import AccountErrorCode, PermissionGroupErrorCode
from ....app.error_codes import AppErrorCode
from ....core.error_codes import SiteErrorCode
from ....invoice.error_codes import InvoiceErrorCode
from ....menu.error_codes import MenuErrorCode
from ....order.error_codes import OrderErrorCode
from ....payment.error_codes import PaymentErrorCode
from ....plugins.error_codes import PluginErrorCode

DJANGO_VALIDATORS_ERROR_CODES = [
    "invalid",
    "invalid_extension",
    "limit_value",
    "max_decimal_places",
    "max_digits",
    "max_length",
    "max_value",
    "max_whole_digits",
    "min_length",
    "min_value",
    "null_characters_not_allowed",
]

DJANGO_FORM_FIELDS_ERROR_CODES = [
    "contradiction",
    "empty",
    "incomplete",
    "invalid_choice",
    "invalid_date",
    "invalid_image",
    "invalid_list",
    "invalid_time",
    "missing",
    "overflow",
]


KOYTOLA_ERROR_CODE_ENUMS = [
    AccountErrorCode,
    AppErrorCode,
    PluginErrorCode,
    InvoiceErrorCode,
    MenuErrorCode,
    OrderErrorCode,
    PaymentErrorCode,
    PermissionGroupErrorCode,
    SiteErrorCode,
]

koytola_error_codes = []
for enum in KOYTOLA_ERROR_CODE_ENUMS:
    koytola_error_codes.extend([code.value for code in enum])


def get_error_code_from_error(error) -> str:
    """Return valid error code from ValidationError.

    It unifies default Django error codes and checks
    if error code is valid.
    """
    code = error.code
    if code in ["required", "blank", "null"]:
        return "required"
    if code in ["unique", "unique_for_date"]:
        return "unique"
    if code in DJANGO_VALIDATORS_ERROR_CODES or code in DJANGO_FORM_FIELDS_ERROR_CODES:
        return "invalid"
    if isinstance(code, Enum):
        code = code.value
    if code not in koytola_error_codes:
        return "invalid"
    return code
