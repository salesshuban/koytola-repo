import graphene

from ...core.permissions import SitePermissions
from ...blog.models import Blog
from ...menu.models import MenuItem
from ...page.models import Page
from ..core.connection import CountableConnection
from ..core.fields import BaseConnectionField
from ..decorators import permission_required
from ..blog.resolvers import resolve_blogs
from ..menu.resolvers import resolve_menu_items
from ..page.resolvers import resolve_pages
# from ..profile.resolvers import resolve_profiles
from ..translations import types as translation_types


class TranslatableItem(graphene.Union):
    class Meta:
        types = (
            translation_types.BlogTranslatableContent,
            translation_types.PageTranslatableContent,
            # translation_types.ProfileTranslatableContent,
            translation_types.MenuItemTranslatableContent,
        )


class TranslatableItemConnection(CountableConnection):
    class Meta:
        node = TranslatableItem


class TranslatableKinds(graphene.Enum):
    BLOG = "Blog"
    PAGE = "Page"
    PROFILE = "Profile"
    MENU_ITEM = "MenuItem"


class TranslationQueries(graphene.ObjectType):
    translations = BaseConnectionField(
        TranslatableItemConnection,
        description="Returns a list of all translatable items of a given kind.",
        kind=graphene.Argument(
            TranslatableKinds, required=True, description="Kind of objects to retrieve."
        ),
    )
    translation = graphene.Field(
        TranslatableItem,
        id=graphene.Argument(
            graphene.ID, description="ID of the object to retrieve.", required=True
        ),
        kind=graphene.Argument(
            TranslatableKinds,
            required=True,
            description="Kind of the object to retrieve.",
        ),
    )

    def resolve_translations(self, info, kind, **_kwargs):
        if kind == TranslatableKinds.BLOG:
            return resolve_blogs(info, query=None)
        elif kind == TranslatableKinds.PAGE:
            return resolve_pages(info, query=None)
        # elif kind == TranslatableKinds.PROFILE:
        #     return resolve_profiles(info, query=None)
        elif kind == TranslatableKinds.MENU_ITEM:
            return resolve_menu_items(info, query=None)

    @permission_required(SitePermissions.MANAGE_TRANSLATIONS)
    def resolve_translation(self, info, id, kind, **_kwargs):
        _type, kind_id = graphene.Node.from_global_id(id)
        if not _type == kind:
            return None
        models = {
            TranslatableKinds.BLOG.value: Blog,
            TranslatableKinds.PAGE.value: Page,
            TranslatableKinds.MENU_ITEM.value: MenuItem,
        }
        return models[kind].objects.filter(pk=kind_id).first()
