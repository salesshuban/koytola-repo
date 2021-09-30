import graphene

from ...account import error_codes as account_error_codes
from ...analytics import error_codes as analytics_error_codes
from ...app import error_codes as app_error_codes
from ...blog import error_codes as blog_error_codes
from ...core import JobStatus, error_codes as core_error_codes
from ...core.permissions import get_permissions_enum_list
from ...helpdesk import error_codes as helpdesk_error_codes
from ...invoice import error_codes as invoice_error_codes
from ...menu import error_codes as menu_error_codes
from ...news import error_codes as news_error_codes
from ...order import error_codes as order_error_codes
from ...page import error_codes as page_error_codes
from ...payment import error_codes as payment_error_codes
from ...profile import error_codes as profile_error_codes
from ...product import error_codes as product_error_codes
from ...plugins import error_codes as plugin_error_codes
from ...webhook import error_codes as webhook_error_codes
from .utils import str_to_enum


class OrderDirection(graphene.Enum):
    ASC = ""
    DESC = "-"

    @property
    def description(self):
        # Disable all the no-member violations in this function
        # pylint: disable=no-member
        if self == OrderDirection.ASC:
            return "Specifies an ascending sort order."
        if self == OrderDirection.DESC:
            return "Specifies a descending sort order."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ReportingPeriod(graphene.Enum):
    TODAY = "TODAY"
    THIS_MONTH = "THIS_MONTH"


def to_enum(enum_cls, *, type_name=None, **options) -> graphene.Enum:
    """Create a Graphene enum from a class containing a set of options.

    :param enum_cls:
        The class to build the enum from.
    :param type_name:
        The name of the type. Default is the class name + 'Enum'.
    :param options:
        - description:
            Contains the type description (default is the class's docstring)
        - deprecation_reason:
            Contains the deprecation reason.
            The default is enum_cls.__deprecation_reason__ or None.
    :return:
    """

    # note this won't work until
    # https://github.com/graphql-python/graphene/issues/956 is fixed
    deprecation_reason = getattr(enum_cls, "__deprecation_reason__", None)
    if deprecation_reason:
        options.setdefault("deprecation_reason", deprecation_reason)

    type_name = type_name or (enum_cls.__name__ + "Enum")
    enum_data = [(str_to_enum(code.upper()), code) for code, name in enum_cls.CHOICES]
    return graphene.Enum(type_name, enum_data, **options)


JobStatusEnum = to_enum(JobStatus)
PermissionEnum = graphene.Enum("PermissionEnum", get_permissions_enum_list())
AccountErrorCode = graphene.Enum.from_enum(account_error_codes.AccountErrorCode)
AnalyticsErrorCode = graphene.Enum.from_enum(analytics_error_codes.AnalyticsErrorCode)
AppErrorCode = graphene.Enum.from_enum(app_error_codes.AppErrorCode)
BlogErrorCode = graphene.Enum.from_enum(blog_error_codes.BlogErrorCode)
PluginErrorCode = graphene.Enum.from_enum(plugin_error_codes.PluginErrorCode)
MenuErrorCode = graphene.Enum.from_enum(menu_error_codes.MenuErrorCode)
MetadataErrorCode = graphene.Enum.from_enum(core_error_codes.MetadataErrorCode)
NewsErrorCode = graphene.Enum.from_enum(news_error_codes.NewsErrorCode)
OrderErrorCode = graphene.Enum.from_enum(order_error_codes.OrderErrorCode)
HelpdeskErrorCode = graphene.Enum.from_enum(helpdesk_error_codes.HelpdeskErrorCode)
InvoiceErrorCode = graphene.Enum.from_enum(invoice_error_codes.InvoiceErrorCode)
PageErrorCode = graphene.Enum.from_enum(page_error_codes.PageErrorCode)
PaymentErrorCode = graphene.Enum.from_enum(payment_error_codes.PaymentErrorCode)
PermissionGroupErrorCode = graphene.Enum.from_enum(
    account_error_codes.PermissionGroupErrorCode
)
ProfileErrorCode = graphene.Enum.from_enum(profile_error_codes.ProfileErrorCode)
ProductErrorCode = graphene.Enum.from_enum(product_error_codes.ProductErrorCode)
SiteErrorCode = graphene.Enum.from_enum(core_error_codes.SiteErrorCode)
TranslationErrorCode = graphene.Enum.from_enum(core_error_codes.TranslationErrorCode)
WebhookErrorCode = graphene.Enum.from_enum(webhook_error_codes.WebhookErrorCode)
