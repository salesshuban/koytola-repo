from ...news.models import News
from ..core.dataloaders import DataLoader


class NewsByIdLoader(DataLoader):
    context_key = "news_by_id"

    def batch_load(self, keys):
        news = News.objects.visible_to_user(self.user).in_bulk(keys)
        return [news.get(news_id) for news_id in keys]
