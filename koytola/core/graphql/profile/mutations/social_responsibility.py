import graphene
from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, SocialResponsibility
from ..utils import company_permission


class SocialResponsibilityInput(graphene.InputObjectType):
    name = graphene.String(description="Company social responsibility name.")
    video = Upload(
        description="Company social responsibility video file.",
        required=False
    )
    youtube_url = graphene.String(description="The youtube url of company social responsibility.")
    image = Upload(
        description="Company social responsibility image file.",
        required=False
    )
    brochure = Upload(
        description="Company social responsibility brochure file.",
        required=False
    )
    description = graphene.String(description="The description of company social responsibility.")
    sort_order = graphene.Int(description="The order of your social responsibility.")
    brochure_file_name = graphene.String(
        description="The name of company social responsibility brochure file.",
        required=False
    )


class SocialResponsibilityCreate(ModelMutation):
    socialResponsibility = graphene.Field(
        SocialResponsibility, description="A created social responsibility."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add social responsibility."
        )
        input = SocialResponsibilityInput(
            required=True, description="Fields required to create a social responsibility."
        )

    class Meta:
        description = "Creates a new social responsibility."
        model = models.SocialResponsibility
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, company_id, **data):
        for file in info.context.FILES:
            if '.pdf' in info.context.FILES[file].name:
                data['brochure_file_name'] = info.context.FILES[file].name
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        company_permission(info, company)
        instance = cls.get_instance(info, **data)
        instance.company = company
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return SocialResponsibilityCreate(socialResponsibility=instance)

    @classmethod
    def get_type_for_model(cls):
        return SocialResponsibility


class SocialResponsibilityUpdate(ModelMutation):
    socialResponsibility = graphene.Field(
        SocialResponsibility, description="An updated social responsibility."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a social responsibility to update."
        )
        input = SocialResponsibilityInput(
            required=True, description="Fields required to update a social responsibility."
        )

    class Meta:
        description = "Updates an existing social responsibility."
        model = models.SocialResponsibility
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        social_responsibility = cls.get_node_or_error(info, id, only_type=SocialResponsibility, field="id")
        company_permission(info, social_responsibility.company)
        cleaned_input = cls.clean_input(info, social_responsibility, data.get("input"))
        if "image" in cleaned_input and not cleaned_input['image']:
            cleaned_input.pop('image')
        if "video" in cleaned_input and not cleaned_input['video']:
            cleaned_input.pop('video')
        if "brochure" in cleaned_input and not cleaned_input['brochure']:
            cleaned_input.pop('brochure')
        instance = cls.construct_instance(social_responsibility, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return SocialResponsibilityUpdate(socialResponsibility=instance)

    @classmethod
    def get_type_for_model(cls):
        return SocialResponsibility


class SocialResponsibilityDelete(ModelDeleteMutation):
    socialResponsibility = graphene.Field(
        SocialResponsibility, description="An updated social responsibility."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a social responsibility to delete."
        )

    class Meta:
        description = "Deletes a social responsibility."
        model = models.SocialResponsibility
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        social_responsibility = cls.get_node_or_error(
            info, id, only_type=SocialResponsibility, field="id"
        )
        company_permission(info, social_responsibility.company)
        social_responsibility.delete()
        return SocialResponsibilityDelete(socialResponsibility=social_responsibility)
