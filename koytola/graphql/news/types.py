from graphene import relay

from ...news import models
from ..core.connection import CountableDjangoObjectType
from ..translations.fields import TranslationField
from ..translations.types import NewsTranslation
from .enums import NewsAudienceTypeEnum


class News(CountableDjangoObjectType):
    audience = NewsAudienceTypeEnum(description="News audience type.")
    translation = TranslationField(NewsTranslation, type_name="news")

    class Meta:
        description = (
            "A news that can be manually added by an admin through the "
            "dashboard."
        )
        only_fields = [
            "content",
            "description",
            "creation_date",
            "summary",
            "id",
            "link",
            "publication_date",
            "is_published",
            "publication_date",
            "update_date",
            "seo_description",
            "seo_title",
            "slug",
            "title",
        ]
        interfaces = [relay.Node]
        model = models.News
