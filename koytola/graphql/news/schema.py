import graphene

from ..core.fields import FilterInputConnectionField
from ..translations.mutations import NewsTranslate
from .bulk_mutations import NewsBulkDelete, NewsBulkPublish
from .filters import NewsFilterInput
from .mutations import NewsCreate, NewsDelete, NewsUpdate
from .resolvers import resolve_news, resolve_news_all
from .sorters import NewsSortingInput
from .types import News


class NewsQueries(graphene.ObjectType):
    news = graphene.Field(
        News,
        id=graphene.Argument(graphene.ID, description="ID of the news."),
        slug=graphene.String(description="The slug of the news."),
        description="Look up a news by ID or slug.",
    )
    news_all = FilterInputConnectionField(
        News,
        sort_by=NewsSortingInput(description="Sort news."),
        filter=NewsFilterInput(description="Filtering options for news."),
        description="List of the all news.",
    )

    def resolve_news(self, info, id=None, slug=None):
        return resolve_news(info, id, slug)

    def resolve_news_all(self, info, **kwargs):
        from ...core.utils.random_data import google_news_create
        google_news_create()
        return resolve_news_all(info, **kwargs)


class NewsMutations(graphene.ObjectType):
    news_create = NewsCreate.Field()
    news_delete = NewsDelete.Field()
    news_bulk_delete = NewsBulkDelete.Field()
    news_bulk_publish = NewsBulkPublish.Field()
    news_update = NewsUpdate.Field()
    news_translate = NewsTranslate.Field()
