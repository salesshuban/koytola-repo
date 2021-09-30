from enum import Enum
from typing import Iterable, List

from django.contrib.auth.models import Permission


class BasePermissionEnum(Enum):
    @property
    def codename(self):
        return self.value.split(".")[1]


class AccountPermissions(BasePermissionEnum):
    MANAGE_USERS = "account.manage_users"
    MANAGE_STAFF = "account.manage_staff"
    MANAGE_ACCOUNT_EVENTS = "account.manage_account_events"


class AnalyticsPermissions(BasePermissionEnum):
    MANAGE_TRACKING = "analytics.manage_tracking"


class AppPermission(BasePermissionEnum):
    MANAGE_APPS = "app.manage_apps"


class BlogPermissions(BasePermissionEnum):
    MANAGE_BLOGS = "blog.manage_blogs"
    MANAGE_BLOG_CATEGORIES = "blog.manage_categories"


class HelpdeskPermissions(BasePermissionEnum):
    MANAGE_TICKETS = "helpdesk.manage_tickets"


class PluginsPermissions(BasePermissionEnum):
    MANAGE_PLUGINS = "plugins.manage_plugins"


class MenuPermissions(BasePermissionEnum):
    MANAGE_MENUS = "menu.manage_menus"


class NewsPermissions(BasePermissionEnum):
    MANAGE_NEWS = "news.manage_news"


class PagePermissions(BasePermissionEnum):
    MANAGE_PAGES = "page.manage_pages"
    MANAGE_PAGE_TYPES = "page.manage_page_types"


class ProfilePermissions(BasePermissionEnum):
    MANAGE_PROFILES = "profile.manage_profiles"
    MANAGE_SUCCESS_STORY = "profile.manage_success_story"


class ProductPermissions(BasePermissionEnum):
    MANAGE_PRODUCTS = "product.manage_products"
    MANAGE_CATEGORIES = "product.manage_categories"


class OrderPermissions(BasePermissionEnum):
    MANAGE_ORDERS = "order.manage_orders"


class SitePermissions(BasePermissionEnum):
    MANAGE_SETTINGS = "site.manage_settings"
    MANAGE_TRANSLATIONS = "site.manage_translations"
    MANAGE_CONTACT_MESSAGES = "site.manage_contact_messages"
    MANAGE_SITE_IMAGES = "site.manage_site_images"
    MANAGE_SITE_SUBSCRIBERS = "site.manage_site_subscribers"


PERMISSIONS_ENUMS = [
    AccountPermissions,
    AnalyticsPermissions,
    AppPermission,
    BlogPermissions,
    HelpdeskPermissions,
    PluginsPermissions,
    MenuPermissions,
    NewsPermissions,
    PagePermissions,
    ProfilePermissions,
    ProductPermissions,
    OrderPermissions,
    SitePermissions,
]


def split_permission_codename(permissions):
    return [permission.split(".")[1] for permission in permissions]


def get_permissions_codename():
    permissions_values = [
        enum.codename
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    ]
    return permissions_values


def get_permissions_enum_dict():
    return {
        enum.name: enum
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    }


def get_permissions_from_names(names: List[str]):
    """Convert list of permission names - ['MANAGE_ORDERS'] to Permission db objects."""
    permissions = get_permissions_enum_dict()
    return get_permissions([permissions[name].value for name in names])


def get_permission_names(permissions: Iterable["Permission"]):
    """Convert Permissions db objects to list of Permission enums."""
    permission_dict = get_permissions_enum_dict()
    names = set()
    for perm in permissions:
        for _, perm_enum in permission_dict.items():
            if perm.codename == perm_enum.codename:
                names.add(perm_enum.name)
    return names


def get_permissions_enum_list():
    permissions_list = [
        (enum.name, enum.value)
        for permission_enum in PERMISSIONS_ENUMS
        for enum in permission_enum
    ]
    return permissions_list


def get_permissions(permissions=None):
    if permissions is None:
        codenames = get_permissions_codename()
    else:
        codenames = split_permission_codename(permissions)
    return (
        Permission.objects.filter(codename__in=codenames)
        .prefetch_related("content_type")
        .order_by("codename")
    )
