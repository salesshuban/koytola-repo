import graphene
from django.core.exceptions import ValidationError

from ...core.permissions import SitePermissions
from ...blog import models as blog_models
from ...menu import models as menu_models
from ...news import models as news_models
from ...page import models as page_models
from ..core.mutations import BaseMutation, ModelMutation, registry
from ..core.types.common import TranslationError
from ..site.types import Site
from .enums import LanguageCodeEnum
from .types import (
    BlogTranslatableContent,
    MenuItemTranslatableContent,
    NewsTranslatableContent,
    PageTranslatableContent,
)


class BaseTranslateMutation(ModelMutation):
    class Meta:
        abstract = True

    @classmethod
    def check_permissions(cls, context):
        return context.user.has_perm(SitePermissions.MANAGE_TRANSLATIONS)

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        if "id" in data and not data["id"]:
            raise ValidationError(
                {"id": ValidationError("This field is required", code="required")}
            )

        model_type = registry.get_type_for_model(cls._meta.model)
        instance = cls.get_node_or_error(info, data["id"], only_type=model_type)
        instance.translations.update_or_create(
            language_code=data["language_code"], defaults=data["input"]
        )
        return cls(**{cls._meta.return_field_name: instance})


class NameTranslationInput(graphene.InputObjectType):
    name = graphene.String()


class SeoTranslationInput(graphene.InputObjectType):
    seo_title = graphene.String()
    seo_description = graphene.String()


class TranslationInput(NameTranslationInput, SeoTranslationInput):
    description = graphene.JSONString()


class MenuItemTranslate(BaseTranslateMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Menu Item ID.")
        language_code = graphene.Argument(
            LanguageCodeEnum, required=True, description="Translation language code."
        )
        input = NameTranslationInput(required=True)

    class Meta:
        description = "Creates/Updates translations for Menu Item."
        model = menu_models.MenuItem
        error_type_class = TranslationError
        error_type_field = "translation_errors"

    @classmethod
    def get_type_for_model(cls):
        return MenuItemTranslatableContent


class BlogTranslationInput(SeoTranslationInput):
    title = graphene.String()
    description = graphene.JSONString()
    content = graphene.JSONString()


class BlogTranslate(BaseTranslateMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Blog ID.")
        language_code = graphene.Argument(
            LanguageCodeEnum, required=True, description="Translation language code."
        )
        input = BlogTranslationInput(required=True)

    class Meta:
        description = "Creates/Updates translations for Blog."
        model = blog_models.Blog
        error_type_class = TranslationError
        error_type_field = "translation_errors"

    @classmethod
    def get_type_for_model(cls):
        return BlogTranslatableContent


class NewsTranslationInput(SeoTranslationInput):
    title = graphene.String()
    summary = graphene.String()
    content = graphene.JSONString()


class NewsTranslate(BaseTranslateMutation):
    class Arguments:
        id = graphene.ID(required=True, description="News ID.")
        language_code = graphene.Argument(
            LanguageCodeEnum, required=True, description="Translation language code."
        )
        input = NewsTranslationInput(required=True)

    class Meta:
        description = "Creates/Updates translations for News."
        model = news_models.News
        error_type_class = TranslationError
        error_type_field = "translation_errors"

    @classmethod
    def get_type_for_model(cls):
        return NewsTranslatableContent


class PageTranslationInput(SeoTranslationInput):
    title = graphene.String()
    description = graphene.JSONString()
    content = graphene.JSONString()


class PageTranslate(BaseTranslateMutation):
    class Arguments:
        id = graphene.ID(required=True, description="Page ID.")
        language_code = graphene.Argument(
            LanguageCodeEnum, required=True, description="Translation language code."
        )
        input = PageTranslationInput(required=True)

    class Meta:
        description = "Creates/Updates translations for Page."
        model = page_models.Page
        error_type_class = TranslationError
        error_type_field = "translation_errors"

    @classmethod
    def get_type_for_model(cls):
        return PageTranslatableContent


class SiteSettingsTranslationInput(graphene.InputObjectType):
    header_text = graphene.String()
    description = graphene.String()


class SiteSettingsTranslate(BaseMutation):
    site = graphene.Field(Site, description="Updated site.")

    class Arguments:
        language_code = graphene.Argument(
            LanguageCodeEnum, required=True, description="Translation language code."
        )
        input = SiteSettingsTranslationInput(
            description="Fields required to update site settings translations.",
            required=True,
        )

    class Meta:
        description = "Creates/Updates translations for Site Settings."
        permissions = (SitePermissions.MANAGE_TRANSLATIONS,)
        error_type_class = TranslationError
        error_type_field = "translation_errors"

    @classmethod
    def perform_mutation(cls, _root, info, language_code, **data):
        instance = info.context.site.settings
        instance.translations.update_or_create(
            language_code=language_code, defaults=data.get("input")
        )
        return SiteSettingsTranslate(site=Site())


