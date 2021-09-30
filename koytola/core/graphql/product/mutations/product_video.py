import graphene
from ....product import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProductError
from ...product.types import Product, ProductVideo
from ..utils import product_permission


class ProductVideoInput(graphene.InputObjectType):
    video = Upload(required=True, description="Product video.")
    alt_text = graphene.String(description="Product video alt text.")
    order = graphene.Int(description="Product video ordering number.")


class ProductVideoCreate(ModelMutation):
    product_video = graphene.Field(
        ProductVideo, description="A created product video."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to add product video."
        )
        input = ProductVideoInput(
            required=True, description="Fields required to create a product video."
        )

    class Meta:
        description = "Creates a new product video."
        model = models.ProductVideo
        error_type_class = ProductError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product_video = models.ProductVideo.objects.create(product=product)
        cleaned_input = cls.clean_input(info, product_video, data.get("input"))
        product_video = cls.construct_instance(product_video, cleaned_input)
        cls.clean_instance(info, product_video)
        cls.save(info, product_video, cleaned_input)
        return ProductVideoCreate(product_video=product_video)


class ProductVideoUpdate(ModelMutation):
    product_video = graphene.Field(ProductVideo, description="An updated product video.")

    class Arguments:
        product_video_id = graphene.ID(
            required=True, description="ID of a product video to update."
        )
        input = ProductVideoInput(
            required=True, description="Fields required to update a product video."
        )

    class Meta:
        description = "Updates an existing product video."
        model = models.ProductVideo
        error_type_class = ProductError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_video_id, **data):
        product_video = cls.get_node_or_error(
            info, product_video_id, only_type=ProductVideo, field="product_video_id"
        )
        product_permission(info, product_video.product)
        cleaned_input = cls.clean_input(info, product_video, data.get("input"))
        product_video = cls.construct_instance(product_video, cleaned_input)
        cls.clean_instance(info, product_video)
        cls.save(info, product_video, cleaned_input)
        return ProductVideoUpdate(product_video=product_video)


class ProductVideoDelete(ModelDeleteMutation):
    class Arguments:
        product_video_id = graphene.ID(
            required=True, description="ID of a product video to delete."
        )

    class Meta:
        description = "Deletes a product video."
        model = models.ProductVideo
        error_type_class = ProductError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_video_id, **data):
        product_video = cls.get_node_or_error(
            info, product_video_id, only_type=ProductVideo, field="product_video_id"
        )
        product_permission(info, product_video.product)
        product_video.delete()
        return ProductVideoDelete(product_video=product_video)
