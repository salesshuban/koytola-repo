from ...blog.models import Blog
from ..core.dataloaders import DataLoader


class BlogByIdLoader(DataLoader):
    context_key = "blog_by_id"

    def batch_load(self, keys):
        blogs = Blog.objects.visible_to_user(self.user).in_bulk(keys)
        return [blogs.get(blog_id) for blog_id in keys]
