import graphene
from ..utils.filters import filter_by_query_param

from ...blog import models

CATEGORY_SEARCH_FIELDS = ("name",)


def resolve_blog_category(info, category_id=None, slug=None):
    assert category_id or slug, "No blog ID or slug provided."
    user = info.context.user
    if slug is not None:
        category = models.Blog.objects.visible_to_user(user).filter(slug=slug).first()
    else:
        _type, category_pk = graphene.Node.from_global_id(category_id)
        category = models.BlogCategory.objects.visible_to_user(user).filter(pk=category_pk).first()
    return category


def resolve_blog_categories(info, query, **_kwargs):
    qs = models.BlogCategory.objects.filter(parent=None)
    return filter_by_query_param(qs, query, CATEGORY_SEARCH_FIELDS)


def resolve_blog(info, global_blog_id=None, slug=None):
    assert global_blog_id or slug, "No blog ID or slug provided."
    user = info.context.user

    if slug is not None:
        blog = models.Blog.objects.visible_to_user(user).filter(slug=slug).first()
    else:
        _type, blog_pk = graphene.Node.from_global_id(global_blog_id)
        blog = models.Blog.objects.visible_to_user(user).filter(pk=blog_pk).first()
    return blog


def resolve_blogs(info, **_kwargs):
    if info.context.user.is_superuser or info.context.user.is_staff:
        return models.Blog.objects.filter()
    return models.Blog.objects.filter(is_active=True, is_published=True)