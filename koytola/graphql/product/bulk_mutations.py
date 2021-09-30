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
        model = models.Product
        permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def bulk_action(cls, queryset, is_active):
        queryset.update(is_active=is_active)


class ProductBulkPublish(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company products to update."
        )

    class Meta:
        description = "Updates company products."
        model = models.Product
        # permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def bulk_action(cls, queryset):
        queryset.update(is_published=True)


class ProductBulkUnpublish(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company products to update."
        )

    class Meta:
        description = "Unpublish company products."
        model = models.Product
        # permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def bulk_action(cls, queryset):
        queryset.update(is_published=False)
