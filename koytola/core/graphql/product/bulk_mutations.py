import graphene
from ..product.types import Product
from ...core.permissions import ProductPermissions
from ...product import models
from ..core.mutations import ModelBulkDeleteMutation, BaseBulkMutation
from ..core.types.common import ProductError
from ..product.utils import product_permission


class ProductBulkDelete(ModelBulkDeleteMutation):

    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company products to delete."
        )

    class Meta:
        description = "Deletes company products."
        model = models.Product
        # permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    # @classmethod
    # def perform_mutation(cls, root, info, ids, **data):
    #     d = None
    #     for product_id in ids:
    #         print(product_id)
    #         product = cls.get_node_or_error(info, product_id, only_type=Product, field="product_id")
    #         product_permission(info, product)
    #         d = product
    #         product.delete()
    #     return ProductBulkDelete(product=d)


class ProductBulkUpdate(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company products to update."
        )
        is_active = graphene.Boolean(
            required=True, description="Update the status of company products."
        )

    class Meta:
        description = "Updates company products."
        model = Product
        permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def bulk_action(cls, queryset, is_active):
        queryset.update(is_active=is_active)
