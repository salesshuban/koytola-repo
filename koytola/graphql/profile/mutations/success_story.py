import graphene
from django.core.exceptions import ValidationError
from ....profile import models
from ....profile.error_codes import ProfileErrorCode
from ...core.types import Upload
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ProfileError
from ...core.utils import (
    validate_slug_and_generate_if_needed
)
from ...profile.types import SuccessStory
from ....core.utils import generate_unique_slug
from ....core.permissions import ProfilePermissions
from ...core.mutations import ModelBulkDeleteMutation


class SuccessStoryInput(graphene.InputObjectType):
    title = graphene.String(description="Success Story Title")
    name = graphene.String(description="Success Story Name")
    description = graphene.String(description="Success Story Description")
    image = Upload(description="Success Story file.")
    location = graphene.String(description="Success Story Title")
    company_name = graphene.String(description="Success Story Company Name")
    tags = graphene.List(graphene.String, description="Success Story tags")
    is_published = graphene.Boolean(description="Success Story tags")


class SuccessStoryCreate(ModelMutation):
    success_story = graphene.Field(SuccessStory, description="An updated success story.")

    class Arguments:
        input = SuccessStoryInput(required=True, description="Fields required to create a Success Story.")

    class Meta:
        description = "Creates a new company."
        model = models.SuccessStory
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def clean_input(cls, info, instance, data):

        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(instance, "title", cleaned_input)
        except ValidationError as error:
            error.code = ProfileErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        return cleaned_input

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        instance.user = info.context.user
        return instance

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()


class SuccessStoryUpdate(ModelMutation):
    successStory = graphene.Field(SuccessStory, description="An updated success story.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a company to update.")
        input = SuccessStoryInput(required=True, description="Fields required to update a company.")

    class Meta:
        description = "Updates an existing Success Story."
        model = models.SuccessStory
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        if 'title' in cleaned_input:
            cleaned_input['slug'] = generate_unique_slug(instance, cleaned_input['title'])
        if 'image' not in cleaned_input or not cleaned_input['image']:
            cleaned_input.pop('image')
        return cleaned_input

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        success_story = cls.get_node_or_error(info, id, only_type=SuccessStory, field="id")
        cleaned_input = cls.clean_input(info, success_story, data.get("input"))
        success_story = cls.construct_instance(success_story, cleaned_input)
        cls.clean_instance(info, success_story)
        cls.save(info, success_story, cleaned_input)
        return SuccessStoryUpdate(successStory=success_story)


class SuccessStoryActivate(ModelMutation):
    successStory = graphene.Field(SuccessStory, description="An Activate success story.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a company to activate.")

    class Meta:
        description = "Activates a company."
        model = models.SuccessStory
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        success_story = cls.get_node_or_error(info, id, only_type=SuccessStory, field="id")
        success_story.is_active = True
        success_story.save()
        return SuccessStoryActivate(successStory=success_story)


class SuccessStoryDeactivate(ModelMutation):
    successStory = graphene.Field(SuccessStory, description="An Deactivate success story.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a success story to Deactivate.")

    class Meta:
        description = "Deactivate a success story."
        model = models.SuccessStory
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        success_story = cls.get_node_or_error(info, id, only_type=SuccessStory, field="id")
        success_story.is_active = False
        success_story.save()
        return SuccessStoryDeactivate(successStory=success_story)


class SuccessStoryDelete(ModelDeleteMutation):
    successStory = graphene.Field(SuccessStory, description="An Delete success story.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a success story to Delete.")

    class Meta:
        description = "Delete a success story."
        model = models.SuccessStory
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        success_story = cls.get_node_or_error(info, id, only_type=SuccessStory, field="id")
        success_story.delete()
        return SuccessStoryDeactivate(successStory=success_story)


class SuccessStoryBulkDelete(ModelBulkDeleteMutation):

    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company Success Story to delete."
        )

    class Meta:
        description = "Deletes company Success Story."
        model = models.SuccessStory
        error_type_class = ProfileError
        error_type_field = "profile_errors"

