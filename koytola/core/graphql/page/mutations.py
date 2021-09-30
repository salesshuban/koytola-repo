import graphene
from collections import defaultdict
from datetime import date
from django.core.exceptions import ValidationError

from ...core.permissions import PagePermissions
from ...page import models
from ...page.error_codes import PageErrorCode
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types.common import PageError, SeoInput
from ..core.utils import (
    clean_seo_fields,
    validate_slug_and_generate_if_needed
)
from .types import Page, PageType


class PageInput(graphene.InputObjectType):
    page_type = graphene.ID(
        description="ID of the page type that page belongs to.", required=True
    )
    slug = graphene.String(description="Page internal name.")
    title = graphene.String(description="Page title.")
    summary = graphene.String(description="Page summary.")
    content = graphene.JSONString(description="Page content in JSON format.")
    is_published = graphene.Boolean(
        description="Determines if page is visible in the storefront."
    )
    publication_date = graphene.String(
        description="Publication date. ISO 8601 standard."
    )
    seo = SeoInput(description="Search engine optimization fields.")


class PageCreate(ModelMutation):
    class Arguments:
        input = PageInput(
            required=True, description="Fields required to create a page."
        )

    class Meta:
        description = "Creates a new page."
        model = models.Page
        permissions = (PagePermissions.MANAGE_PAGES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "title", cleaned_input
            )
        except ValidationError as error:
            error.code = PageErrorCode.REQUIRED
            raise ValidationError({"slug": error})

        is_published = cleaned_input.get("is_published")
        publication_date = cleaned_input.get("publication_date")
        if is_published and not publication_date:
            cleaned_input["publication_date"] = date.today()

        clean_seo_fields(cleaned_input)

        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return Page


class PageUpdate(PageCreate):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a page to update.")
        input = PageInput(
            required=True, description="Fields required to update a page."
        )

    class Meta:
        description = "Updates an existing page."
        model = models.Page
        permissions = (PagePermissions.MANAGE_PAGES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def get_type_for_model(cls):
        return Page


class PageDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a page to delete.")

    class Meta:
        description = "Deletes a page."
        model = models.Page
        permissions = (PagePermissions.MANAGE_PAGES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def get_type_for_model(cls):
        return Page


class PageTypeCreateInput(graphene.InputObjectType):
    name = graphene.String(description="Name of the page type.")
    slug = graphene.String(description="Page type slug.")
    add_attributes = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of attribute IDs to be assigned to the page type.",
    )


class PageTypeUpdateInput(PageTypeCreateInput):
    remove_attributes = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of attribute IDs to be assigned to the page type.",
    )


class PageTypeCreate(ModelMutation):
    class Arguments:
        input = PageTypeCreateInput(
            description="Fields required to create page type.", required=True
        )

    class Meta:
        description = "Create a new page type."
        model = models.PageType
        permissions = (PagePermissions.MANAGE_PAGE_TYPES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        errors = defaultdict(list)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "name", cleaned_input
            )
        except ValidationError as error:
            error.code = PageErrorCode.REQUIRED.value
            errors["slug"].append(error)

        if errors:
            raise ValidationError(errors)

        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return PageType


class PageTypeUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(description="ID of the page type to update.")
        input = PageTypeUpdateInput(
            description="Fields required to update page type.", required=True
        )

    class Meta:
        description = "Update page type."
        model = models.PageType
        permissions = (PagePermissions.MANAGE_PAGE_TYPES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        errors = defaultdict(list)
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "name", cleaned_input
            )
        except ValidationError as error:
            error.code = PageErrorCode.REQUIRED
            errors["slug"].append(error)
        if errors:
            raise ValidationError(errors)

        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return PageType


class PageTypeDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of the page type to delete.")

    class Meta:
        description = "Delete a page type."
        model = models.PageType
        permissions = (PagePermissions.MANAGE_PAGE_TYPES,)
        error_type_class = PageError
        error_type_field = "page_errors"

    @classmethod
    def get_type_for_model(cls):
        return PageType
