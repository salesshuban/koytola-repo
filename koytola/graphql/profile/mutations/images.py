import graphene
from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, Images
from ..utils import company_permission
from ...core.fields import FilterInputConnectionField


class ImageInput(graphene.InputObjectType):
    image = Upload(description="Company image file.", required=False)
    description = graphene.String(description="The description of company image.")
    sort_order = graphene.Int(description="The order of your image.")


class ImageCreate(ModelMutation):
    imgs = FilterInputConnectionField(
        Images, description="A created image."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add image."
        )
        input = ImageInput(
            required=True, description="Fields required to create a image."
        )

    class Meta:
        description = "Creates a new image."
        model = models.Images
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

        return ImageCreate(imgs=models.Images.objects.filter(company=company))

    @classmethod
    def get_type_for_model(cls):
        return Images


class ImageUpdate(ModelMutation):
    image = graphene.Field(Images, description="An updated image.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a image to update."
        )
        input = ImageInput(
            required=True, description="Fields required to update a image."
        )

    class Meta:
        description = "Updates an existing image."
        model = models.Images
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        image = cls.get_node_or_error(
            info, id, only_type=Images, field="id"
        )
        company_permission(info, image.company)
        cleaned_input = cls.clean_input(info, image, data.get("input"))
        contact = cls.construct_instance(image, cleaned_input)
        cls.clean_instance(info, contact)
        cls.save(info, contact, cleaned_input)
        return ImageUpdate(image=image)

    @classmethod
    def get_type_for_model(cls):
        return Images


class ImageDelete(ModelDeleteMutation):
    imgs = FilterInputConnectionField(Images, description="An updated image.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a image to delete."
        )

    class Meta:
        description = "Deletes a image."
        model = models.Images
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        image = cls.get_node_or_error(
            info, id, only_type=Images, field="id"
        )
        company = image.company
        company_permission(info, image.company)
        image.delete()

        return ImageDelete(imgs=models.Images.objects.filter(company=company))


class ImageIndexUpdate(ModelMutation):
    imgs = FilterInputConnectionField(Images, description="An updated image.")

    class Arguments:
        ids = graphene.List(graphene.ID, required=True, description="Product images.")

    class Meta:
        description = "image index update."
        model = models.Images
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, ids, **data):
        image_list = []
        for index, id in enumerate(ids):
            image = cls.get_node_or_error(info, id, only_type=Images, field="id")
            company_permission(info, image.company)
            image.index = index
            image.save()
            image_list.append(image)
        return ImageIndexUpdate(imgs=image_list)
