import graphene
from graphene_federation import key

from ...core.permissions import PagePermissions
from ...page import models
from ..core.connection import CountableDjangoObjectType
from ..decorators import permission_required
from ..meta.types import ObjectWithMetadata
from ..translations.fields import TranslationField
from ..translations.types import PageTranslation
from .dataloaders import (
    PagesByPageTypeIdLoader,
    PageTypeByIdLoader,
)


class Page(CountableDjangoObjectType):
    translation = TranslationField(PageTranslation, type_name="page")

    class Meta:
        description = (
            "A static page that can be manually added by a site operator through the "
            "dashboard."
        )
        only_fields = [
            "content",
            "creation_date",
            "id",
            "is_published",
            "page_type",
            "publication_date",
            "seo_description",
            "seo_title",
            "slug",
            "summary",
            "title",
            "update_date",
        ]
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
        model = models.Page

    @staticmethod
    def resolve_page_type(root: models.Page, info):
        return PageTypeByIdLoader(info.context).load(root.page_type_id)


@key(fields="id")
@key(fields="slug")
class PageType(CountableDjangoObjectType):
    has_pages = graphene.Boolean(description="Whether page type has pages assigned.")

    class Meta:
        description = (
            "Represents a type of page."
        )
        interfaces = [graphene.relay.Node, ObjectWithMetadata]
        model = models.PageType
        only_fields = ["id", "name", "slug"]

    @staticmethod
    @permission_required(PagePermissions.MANAGE_PAGES)
    def resolve_has_pages(root: models.PageType, info, **kwargs):
        return (
            PagesByPageTypeIdLoader(info.context)
            .load(root.pk)
            .then(lambda pages: bool(pages))
        )
