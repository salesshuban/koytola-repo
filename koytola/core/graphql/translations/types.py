import graphene
from django.conf import settings

from ...core.permissions import (
    BlogPermissions,
    NewsPermissions,
    PagePermissions,
    SitePermissions
)
from ...blog import models as blog_models
from ...menu import models as menu_models
from ...news import models as news_models
from ...page import models as page_models
from ...site import models as site_models
from ..core.connection import CountableDjangoObjectType
from ..core.types import LanguageDisplay
from ..core.utils import str_to_enum
from ..decorators import permission_required
from .enums import LanguageCodeEnum
from .fields import TranslationField

BASIC_TRANSLATABLE_FIELDS = ["id", "name"]


class BaseTranslationType(CountableDjangoObjectType):
    language = graphene.Field(
        LanguageDisplay, description="Translation language.", required=True
    )

    class Meta:
        abstract = True

    @staticmethod
    def resolve_language(root, *_args):
        try:
            language = next(
                language[1]
                for language in settings.LANGUAGES
                if language[0] == root.language_code
            )
        except StopIteration:
            return None
        return LanguageDisplay(
            code=LanguageCodeEnum[str_to_enum(root.language_code)], language=language
        )


class BlogTranslation(BaseTranslationType):
    class Meta:
        model = blog_models.BlogTranslation
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "id",
            "seo_description",
            "seo_title",
            "summary",
            "title",
        ]


class BlogTranslatableContent(CountableDjangoObjectType):
    translation = TranslationField(BlogTranslation, type_name="blog")
    blog = graphene.Field(
        "koytola.graphql.blog.types.Blog",
        description=(
            "A blog that can be manually added by a site operator ",
            "through the dashboard.",
        ),
    )

    class Meta:
        model = blog_models.Blog
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "id",
            "seo_description",
            "seo_title",
            "summary",
            "title",
        ]

    @staticmethod
    @permission_required(BlogPermissions.MANAGE_BLOGS)
    def resolve_blog(root: blog_models.Blog, info):
        return (
            blog_models.Blog.objects.visible_to_user(info.context.user)
            .filter(pk=root.id)
            .first()
        )


class NewsTranslation(BaseTranslationType):
    class Meta:
        model = news_models.NewsTranslation
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "content_plaintext",
            "id",
            "summary",
            "title",
        ]


class NewsTranslatableContent(CountableDjangoObjectType):
    translation = TranslationField(NewsTranslation, type_name="news")
    news = graphene.Field(
        "koytola.graphql.news.types.News",
        description=(
            "A news that can be manually added by a site operator ",
            "through the dashboard.",
        ),
    )

    class Meta:
        model = news_models.News
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "content_plaintext",
            "id",
            "summary",
            "title",
        ]

    @staticmethod
    @permission_required(NewsPermissions.MANAGE_NEWS)
    def resolve_news(root: news_models.News, info):
        return (
            news_models.News.objects.visible_to_user(info.context.user)
            .filter(pk=root.id)
            .first()
        )


class PageTranslation(BaseTranslationType):
    class Meta:
        model = page_models.PageTranslation
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "id",
            "seo_description",
            "seo_title",
            "title",
            "summary",
        ]


class PageTranslatableContent(CountableDjangoObjectType):
    translation = TranslationField(PageTranslation, type_name="page")
    page = graphene.Field(
        "koytola.graphql.page.types.Page",
        description=(
            "A static page that can be manually added by a site operator ",
            "through the dashboard.",
        ),
    )

    class Meta:
        model = page_models.Page
        interfaces = [graphene.relay.Node]
        only_fields = [
            "content",
            "id",
            "seo_description",
            "seo_title",
            "title",
            "summary",
        ]

    @staticmethod
    @permission_required(PagePermissions.MANAGE_PAGES)
    def resolve_page(root: page_models.Page, info):
        return (
            page_models.Page.objects.visible_to_user(info.context.user)
            .filter(pk=root.id)
            .first()
        )


class SiteTranslation(BaseTranslationType):
    class Meta:
        model = site_models.SiteSettingsTranslation
        interfaces = [graphene.relay.Node]
        only_fields = ["description", "header_text", "id"]


class MenuItemTranslation(BaseTranslationType):
    class Meta:
        model = menu_models.MenuItemTranslation
        interfaces = [graphene.relay.Node]
        only_fields = BASIC_TRANSLATABLE_FIELDS


class MenuItemTranslatableContent(CountableDjangoObjectType):
    translation = TranslationField(MenuItemTranslation, type_name="menu item")
    menu_item = graphene.Field(
        "koytola.graphql.menu.types.MenuItem",
        description=(
            "Represents a single item of the related menu. Can store categories, "
            "collection or pages."
        ),
    )

    class Meta:
        model = menu_models.MenuItem
        interfaces = [graphene.relay.Node]
        only_fields = BASIC_TRANSLATABLE_FIELDS

    @staticmethod
    @permission_required(SitePermissions.MANAGE_SETTINGS)
    def resolve_menu_item(root: menu_models.MenuItem, _info):
        return root
