import graphene
from django.core.exceptions import ValidationError
from ..core.types import Upload
from ...core.permissions import BlogPermissions
from ...blog import models
from ...blog.error_codes import BlogErrorCode
from ..core.mutations import ModelDeleteMutation, ModelMutation
from ..core.types.common import BlogError, SeoInput
from ..core.utils import (
    clean_seo_fields,
    update_publication_date,
    validate_slug_and_generate_if_needed
)
from .types import Blog, BlogCategory


class BlogInput(graphene.InputObjectType):
    category = graphene.String(description="Blog category.")
    title = graphene.String(description="Blog title.")
    slug = graphene.String(description="Blog title.")
    image = Upload(description="blog images file.")
    short_description = graphene.String(description="Blog short description.")
    description = graphene.String(description="Blog description.")
    tags = graphene.List(graphene.String, description="Blog tags.")
    is_published = graphene.Boolean(
        description="Determines if blog is visible in the storefront."
    )
    seo = SeoInput(description="Search engine optimization fields.")


class BlogCreate(ModelMutation):
    blog = graphene.Field(Blog, description="Look up a blog by ID or slug.")

    class Arguments:
        input = BlogInput(
            required=True, description="Fields required to create a blog."
        )

    class Meta:
        description = "Creates a new blog."
        model = models.Blog
        permissions = (BlogPermissions.MANAGE_BLOGS,)
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser or context.user.is_staff

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "title", cleaned_input
            )
        except ValidationError as error:
            error.code = BlogErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input)
        return cleaned_input

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        instance.user = info.context.user
        return instance

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return BlogCreate(blog=instance)

    @classmethod
    def get_type_for_model(cls):
        return Blog


class BlogUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a blog to update.")
        input = BlogInput(
            required=True, description="Fields required to update a blog."
        )

    class Meta:
        description = "Updates an existing blog."
        model = models.Blog
        permissions = (BlogPermissions.MANAGE_BLOGS,)
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        if 'image' not in cleaned_input or not cleaned_input['image'] or not any(cleaned_input['image']):
            cleaned_input.pop('image')
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "title", cleaned_input
            )
        except ValidationError as error:
            error.code = BlogErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input, instance)
        return cleaned_input


class BlogDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a blog to delete.")

    class Meta:
        description = "Deletes a blog."
        model = models.Blog
        permissions = (BlogPermissions.MANAGE_BLOGS,)
        error_type_class = BlogError
        error_type_field = "blog_errors"


class BlogActivate(ModelDeleteMutation):
    blog = graphene.Field(Blog, description="Look up a blog by ID or slug.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Active an existing Offer."
        model = models.Blog
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        blog = cls.get_node_or_error(info, id, only_type=Blog, field="blog_id")
        blog.is_active = True
        blog.save()
        return BlogActivate(blog=blog)


class BlogDeactivate(ModelDeleteMutation):
    blog = graphene.Field(Blog, description="Look up a blog by ID or slug.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Deactivate an existing Offer."
        model = models.Blog
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        blog = cls.get_node_or_error(info, id, only_type=Blog, field="blog_id")
        blog.is_active = False
        blog.save()
        return BlogDeactivate(blog=blog)


class BlogPublish(ModelDeleteMutation):
    blog = graphene.Field(Blog, description="Look up a blog by ID or slug.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Active an existing Offer."
        model = models.Blog
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        blog = cls.get_node_or_error(info, id, only_type=Blog, field="blog_id")
        blog.is_published = True
        blog.save()
        return BlogPublish(blog=blog)


class BlogUnPublish(ModelDeleteMutation):
    blog = graphene.Field(Blog, description="Look up a blog by ID or slug.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Deactivate an existing Offer."
        model = models.Blog
        error_type_class = BlogError
        error_type_field = "blog_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        blog = cls.get_node_or_error(info, id, only_type=Blog, field="blog_id")
        blog.is_published = False
        blog.save()
        return BlogUnPublish(blog=blog)

