import graphene

from ...core.permissions import BlogPermissions
from ...blog import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation
from ..core.types.common import BlogError


class BlogBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of blog IDs to delete."
        )

    class Meta:
        description = "Deletes blogs."
        model = models.Blog
        permissions = (BlogPermissions.MANAGE_BLOGS,)
        error_type_class = BlogError
        error_type_field = "blog_errors"


class BlogBulkPublish(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of blog IDs to (un)publish."
        )
        is_published = graphene.Boolean(
            required=True, description="Determine if blogs will be published or not."
        )

    class Meta:
        description = "Publish blogs."
        model = models.Blog
        permissions = (BlogPermissions.MANAGE_BLOGS,)
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def bulk_action(cls, queryset, is_published):
        queryset.update(is_published=is_published)
