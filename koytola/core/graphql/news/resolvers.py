import graphene

from ...news import models


def resolve_news(info, global_news_id=None, slug=None):
    assert global_news_id or slug, "No news ID or slug provided."

    if slug is not None:
        news = models.News.objects.filter(slug=slug).first()
    else:
        _type, news_pk = graphene.Node.from_global_id(global_news_id)
        news = models.News.objects.filter(pk=news_pk).first()
    return news


def resolve_news_all(info, **_kwargs):
    return models.News.objects.filter(is_active=True)
