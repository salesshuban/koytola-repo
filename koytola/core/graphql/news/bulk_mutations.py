import graphene

from ...core.permissions import NewsPermissions
from ...news import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation
from ..core.types.common import NewsError


class NewsBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of news IDs to delete."
        )

    class Meta:
        description = "Deletes news."
        model = models.News
        permissions = (NewsPermissions.MANAGE_NEWS,)
        error_type_class = NewsError
        error_type_field = "news_errors"


class NewsBulkPublish(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of news IDs to (un)publish."
        )
        is_published = graphene.Boolean(
            required=True, description="Determine if multiple news will be published or not."
        )

    class Meta:
        description = "Publish multiple news."
        model = models.News
        permissions = (NewsPermissions.MANAGE_NEWS,)
        error_type_class = NewsError
        error_type_field = "news_errors"

    @classmethod
    def bulk_action(cls, queryset, is_published):
        queryset.update(is_published=is_published)
