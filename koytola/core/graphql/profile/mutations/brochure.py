import graphene
from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, Brochure
from ..utils import company_permission
from ...core.fields import FilterInputConnectionField


class BrochureInput(graphene.InputObjectType):
    brochure = Upload(description="Company brochure file.", required=False)
    description = graphene.String(description="The description of company brochure.")
    sort_order = graphene.Int(description="The order of your brochure.")


class BrochureCreate(ModelMutation):
    brochures = FilterInputConnectionField(Brochure, description="A created brochure.")

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add brochure."
        )
        input = BrochureInput(
            required=True, description="Fields required to create a brochure."
        )

    class Meta:
        description = "Creates a new brochure."
        model = models.Brochure
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
        instance = cls.get_instance(info, **data)
        instance.company = company
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return BrochureCreate(brochures=models.Brochure.objects.filter(company=company))

    @classmethod
    def get_type_for_model(cls):
        return Brochure


class BrochureUpdate(ModelMutation):
    brochures = FilterInputConnectionField(Brochure, description="A created brochure.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a brochure to update."
        )
        input = BrochureInput(
            required=True, description="Fields required to update a brochure."
        )

    class Meta:
        description = "Updates an existing brochure."
        model = models.Brochure
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        brochure = cls.get_node_or_error(
            info, id, only_type=Brochure, field="id"
        )
        company_permission(info, brochure.company)
        cleaned_input = cls.clean_input(info, brochure, data.get("input"))
        contact = cls.construct_instance(brochure, cleaned_input)
        cls.clean_instance(info, contact)
        cls.save(info, contact, cleaned_input)
        return BrochureUpdate(brochures=models.Brochure.objects.filter(company=company))

    @classmethod
    def get_type_for_model(cls):
        return Brochure


class BrochureDelete(ModelDeleteMutation):
    brochures = FilterInputConnectionField(Brochure, description="A created brochure.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a brochure to delete."
        )

    class Meta:
        description = "Deletes a brochure."
        model = models.Brochure
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        brochure = cls.get_node_or_error(
            info, id, only_type=Brochure, field="id"
        )
        company_permission(info, brochure.company)
        company = brochure.company
        brochure.delete()
        return BrochureDelete(brochures=models.Brochure.objects.filter(company=company))


class BrochureIndexUpdate(ModelMutation):
    brochures = FilterInputConnectionField(Brochure, description="An updated brochure.")

    class Arguments:
        ids = graphene.List(graphene.ID, required=True, description="Company brochure.")

    class Meta:
        description = "Brochure index update."
        model = models.Brochure
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, ids, **data):
        brochure_list = []
        for index, id in enumerate(ids):
            brochure = cls.get_node_or_error(info, id, only_type=Brochure, field="id")
            company_permission(info, brochure.company)
            brochure.index = index
            brochure.save()
            brochure_list.append(brochure)
        return BrochureIndexUpdate(brochures=brochure_list)
