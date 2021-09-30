import graphene
from ....product import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProductError
from ...product.types import Product, ProductReviews
from ..utils import product_permission


class ProductReviewsInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="Product video.")
    rating = graphene.Float(description="Product video alt text.")
    review = graphene.String(required=True, description="Product video.")
    location = graphene.String(required=True, description="Product video.")


class ProductReviewsCreate(ModelMutation):
    product_review = graphene.Field(
        ProductReviews, description="A created product reviews."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to add product video."
        )
        input = ProductReviewsInput(
            required=True, description="Fields required to create a product video."
        )

    class Meta:
        description = "Creates a new product video."
        model = models.ProductReviews
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(info, product_id, only_type=Product, field="product_id")
        product_review = models.ProductReviews.objects.create(product=product)
        product_review.user = info.context.user if info.context.user.is_authenticated else None
        cleaned_input = cls.clean_input(info, product_review, data.get("input"))
        product_review = cls.construct_instance(product_review, cleaned_input)
        cls.clean_instance(info, product_review)
        cls.save(info, product_review, cleaned_input)
        return ProductReviewsCreate(product_review=product_review)
