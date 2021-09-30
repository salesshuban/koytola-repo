import graphene

from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, Representative
from ..utils import company_permission


class RepresentativeInput(graphene.InputObjectType):
    photo = Upload(description="Representative file.")
    name = graphene.String(description="The representative name of your company")
    position = graphene.String(description="The representative position of your company")
    linkedin_url = graphene.String(description="The representative linkedin URL")


class RepresentativeCreate(ModelMutation):
    representative = graphene.Field(
        Representative, description="A created representative."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add representative."
        )
        input = RepresentativeInput(
            required=True, description="Fields required to create a representative."
        )

    class Meta:
        description = "Creates a new representative."
        model = models.Representative
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, company_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        company_permission(info, company)
        representative = models.Representative.objects.create(company=company)
        if "photo" not in data["input"] or not data["input"]["photo"]:
            data["input"].pop("photo")
        cleaned_input = cls.clean_input(info, representative, data.get("input"))
        representative = cls.construct_instance(representative, cleaned_input)
        cls.clean_instance(info, representative)
        cls.save(info, representative, cleaned_input)
        return RepresentativeCreate(representative=representative)


class RepresentativeUpdate(ModelMutation):
    representative = graphene.Field(Representative, description="An updated representative.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a representative to update."
        )
        input = RepresentativeInput(
            required=True, description="Fields required to update a representative."
        )

    class Meta:
        description = "Updates an existing ticket."
        model = models.Representative
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        representative = cls.get_node_or_error(
            info, id, only_type=Representative, field="id"
        )
        company_permission(info, representative.company)
        print(info.context.FILES, type(info.context.FILES))
        cleaned_input = cls.clean_input(info, representative, data.get("input"))
        if 'photo' in cleaned_input and not cleaned_input['photo']:
            cleaned_input.pop('photo')
        representative = cls.construct_instance(representative, cleaned_input)
        cls.clean_instance(info, representative)
        cls.save(info, representative, cleaned_input)
        return RepresentativeUpdate(representative=representative)


class RepresentativeDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a representative to delete."
        )

    class Meta:
        description = "Deletes a representative."
        model = models.Representative
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        representative = cls.get_node_or_error(
            info, id, only_type=Representative, field="id"
        )
        company_permission(info, representative.company)
        representative.delete()
        return RepresentativeDelete(representative=representative)
