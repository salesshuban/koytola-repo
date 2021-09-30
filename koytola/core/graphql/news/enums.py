import graphene

from ...news import NewsAudienceType
from ...graphql.core.enums import to_enum


NewsAudienceTypeEnum = to_enum(NewsAudienceType, type_name="NewsAudienceTypeEnum")


class NewsPublishedStatus(graphene.Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"
