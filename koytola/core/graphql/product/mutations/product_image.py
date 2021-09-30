import graphene

from ....product import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProductError
from ...product.types import Product, ProductImage
from ..utils import product_permission


class ProductImageInput(graphene.InputObjectType):
    # images = graphene.List(Upload, required=True, description="Product images.")
    image = Upload(description="Product image.", required=False)
    alt_text = graphene.String(description="Product image alt text.")
    order = graphene.Int(description="Product image ordering number.")


class ProductImageIndexInput(graphene.InputObjectType):
    ids = graphene.List(graphene.ID, required=True, description="Product images.")


class ProductImageCreate(ModelMutation):
    productImage = graphene.Field(
        ProductImage, description="A created product image."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to add product image."
        )
        input = ProductImageInput(
            required=True, description="Fields required to create a product image."
        )

    class Meta:
        description = "Creates a new product image."
        model = models.ProductImage
        error_type_class = ProductError
        error_type_field = "product_image_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(info, product_id, only_type=Product, field="product_id")
        # images = data['input']['images']
        # data['input'].pop('images')
        # product_images = []
        # for i in images:
        #     data['input']['image'] = i
        product_permission(info, product)
        product_image = models.ProductImage.objects.create(product=product)
        cleaned_input = cls.clean_input(info, product_image, data.get("input"))
        product_image = cls.construct_instance(product_image, cleaned_input)
        cls.clean_instance(info, product_image)
        cls.save(info, product_image, cleaned_input)
        # product_images.append(product_image)
        return ProductImageCreate(productImage=product_image)


class ProductImageUpdate(ModelMutation):
    productImage = graphene.Field(ProductImage, description="An updated product image.")

    class Arguments:
        product_image_id = graphene.ID(
            required=True, description="ID of a product image to update."
        )
        input = ProductImageInput(
            required=True, description="Fields required to update a product image."
        )

    class Meta:
        description = "Updates an existing product image."
        model = models.ProductImage
        error_type_class = ProductError
        error_type_field = "product_image_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_image_id, **data):
        product_image = cls.get_node_or_error(
            info, product_image_id, only_type=ProductImage, field="product_image_id"
        )
        product_permission(info, product_image.product)
        cleaned_input = cls.clean_input(info, product_image, data.get("input"))
        product_image = cls.construct_instance(product_image, cleaned_input)
        cls.clean_instance(info, product_image)
        cls.save(info, product_image, cleaned_input)
        return ProductImageUpdate(productImage=product_image)


class ProductImageDelete(ModelDeleteMutation):
    productImage = graphene.Field(ProductImage, description="An updated product image.")

    class Arguments:
        product_image_id = graphene.ID(
            required=True, description="ID of a product image to delete."
        )

    class Meta:
        description = "Deletes a product image."
        model = models.ProductImage
        error_type_class = ProductError
        error_type_field = "product_image_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_image_id, **data):
        product_image = cls.get_node_or_error(
            info, product_image_id, only_type=ProductImage, field="product_image_id"
        )
        product_permission(info, product_image.product)
        product_image.delete()
        return ProductImageDelete(productImage=product_image)


class ProductImageIndexUpdate(ModelMutation):
    productImageList = graphene.List(ProductImage, description="An updated product image.")

    class Arguments:
        input = ProductImageIndexInput(
            required=True, description="IDs required to update a product image index."
        )

    class Meta:
        description = "Deletes a product image."
        model = models.ProductImage
        error_type_class = ProductError
        error_type_field = "product_image_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, **data):
        product_image_list = []
        for index, product_image_id in enumerate(data['input']['ids']):
            product_image = cls.get_node_or_error(info, product_image_id, only_type=ProductImage,
                                                  field="product_image_id")
            product_permission(info, product_image.product)
            product_image.index = index
            product_image.save()
            product_image_list.append(product_image)
        return ProductImageIndexUpdate(productImageList=product_image_list)
