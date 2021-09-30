import graphene
import requests
from ...news import models
import xmltodict
from datetime import datetime
from django.utils.text import slugify


def resolve_news(info, global_news_id=None, slug=None):
    assert global_news_id or slug, "No news ID or slug provided."

    if slug is not None:
        news = models.News.objects.filter(slug=slug).first()
    else:
        _type, news_pk = graphene.Node.from_global_id(global_news_id)
        news = models.News.objects.filter(pk=news_pk).first()
    return news


def resolve_news_all(info, **_kwargs):
    url = '''https://news.google.com/rss/search?q=trade+site:ft.com+OR+site:bloomberg.com+OR+site:forbes.com+OR+site:theguardian.com&client=safari&rls=en&hl=en-US&gl=US&ceid=US:en'''
    f = requests.get(url)
    news = xmltodict.parse(f.content.decode('utf-8'))
    for i in news['rss']['channel']['item']:
        pub_date = datetime.strptime(i['pubDate'], "%a, %d %b %Y %H:%M:%S %Z")
        if not models.News.objects.filter(slug=slugify(i['title'])).exists():
            models.News(title=i['title'], slug=slugify(i['title']), link=i['link'], publication_date=pub_date, is_active=True).save()
    return models.News.objects.filter(is_active=True)
