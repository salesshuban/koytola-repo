import graphene
from django.core.exceptions import ValidationError

from ...core.permissions import NewsPermissions
from ...news import models
from ...news.error_codes import NewsErrorCode
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types.common import NewsError, SeoInput
from ..core.utils import (
    clean_seo_fields,
    update_publication_date,
    validate_slug_and_generate_if_needed
)
from .enums import NewsAudienceTypeEnum
from .types import News


class NewsInput(graphene.InputObjectType):
    audience = NewsAudienceTypeEnum(description="News audience type.", required=False)
    slug = graphene.String(description="News internal name.")
    title = graphene.String(description="News title.")
    summary = graphene.String(description="News summary.")
    content = graphene.JSONString(description="News content in JSON format.")
    link = graphene.String(description="News content in JSON format.")
    is_published = graphene.Boolean(description="Determines if news is visible in the storefront.")
    is_active = graphene.Boolean(description="Determines if news is visible in the storefront.")
    publication_date = graphene.String(description="Publication date. ISO 8601 standard.")
    seo = SeoInput(description="Search engine optimization fields.")


class NewsCreate(ModelMutation):
    class Arguments:
        input = NewsInput(
            description="Fields required to create a news."
        )

    class Meta:
        description = "Creates a new news."
        model = models.News
        permissions = (NewsPermissions.MANAGE_NEWS,)
        error_type_class = NewsError
        error_type_field = "news_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "title", cleaned_input
            )
        except ValidationError as error:
            error.code = NewsErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input)
        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return News


class NewsUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a news to update.")
        input = NewsInput(
            required=True, description="Fields required to update a news."
        )

    class Meta:
        description = "Updates an existing news."
        model = models.News
        permissions = (NewsPermissions.MANAGE_NEWS,)
        error_type_class = NewsError
        error_type_field = "news_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "title", cleaned_input
            )
        except ValidationError as error:
            error.code = NewsErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input, instance)
        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return News


class NewsDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a news to delete.")

    class Meta:
        description = "Deletes a news."
        model = models.News
        permissions = (NewsPermissions.MANAGE_NEWS,)
        error_type_class = NewsError
        error_type_field = "news_errors"
