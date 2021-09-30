import graphene
from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...core.types.rosetters import Roetter
from ..enums import RosetterType
from ...core.mutations import ModelBulkDeleteMutation


class RosetterInput(graphene.InputObjectType):
    type = RosetterType(description="Rosetter Type")
    name = graphene.String(description="Rosetter name")
    image = Upload(description="Rosetter image file.")
    is_active = graphene.Boolean(description="Rosetter is active")


class RosetterCreate(ModelMutation):
    rosetter = graphene.Field(Roetter, description="A created Roetter." )

    class Arguments:
        input = RosetterInput(
            required=True, description="Fields required to create a social responsibility."
        )

    class Meta:
        description = "Creates a new rosetter."
        model = models.Roetter
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return RosetterCreate(rosetter=instance)

    @classmethod
    def get_type_for_model(cls):
        return Roetter


class RosetterUpdate(ModelMutation):
    rosetter = graphene.Field(Roetter, description="A created Roetter." )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a rosetter to update."
        )
        input = RosetterInput(
            required=True, description="Fields required to create a rosetter."
        )

    class Meta:
        description = "Creates a new rosetter."
        model = models.Roetter
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        rosetter = cls.get_node_or_error(info, id, only_type=Roetter, field="id")
        cleaned_input = cls.clean_input(info, rosetter, data.get("input"))
        instance = cls.construct_instance(rosetter, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return RosetterUpdate(rosetter=instance)

    @classmethod
    def get_type_for_model(cls):
        return Roetter


class RosetterDelete(ModelDeleteMutation):
    rosetter = graphene.Field(Roetter, description="An delete Rosetter.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a social responsibility to delete.")

    class Meta:
        description = "Deletes a rosetter."
        model = models.Roetter
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated and context.user.is_superuser

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        rosetter = cls.get_node_or_error(info, id, only_type=Roetter, field="id")
        rosetter.delete()
        return RosetterDelete(rosetter=rosetter)


class RosetterBulkDelete(ModelBulkDeleteMutation):

    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company Rosetter to delete."
        )

    class Meta:
        description = "Deletes company Rosetter."
        model = models.Roetter
        error_type_class = ProfileError
        error_type_field = "profile_errors"

