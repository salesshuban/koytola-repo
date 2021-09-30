from django.core.exceptions import ValidationError

from ...core.exceptions import PermissionDenied
from ...core.permissions import ProductPermissions
from ...product import models
from ...product.error_codes import ProductErrorCode


def product_permission(info, product):
    # Raise error if the current user doesn't have permission.
    print(info.context)
    if product.company.user and product.company.user != info.context.user:
        if not info.context.user.has_perm(
                ProductPermissions.MANAGE_PRODUCTS
        ):
            raise PermissionDenied()

    # Raise error if the product status is inactive.
    if not product.is_active:
        if not info.context.user.has_perm(ProductPermissions.MANAGE_PRODUCTS):
            raise PermissionDenied()


def clean_product_slug(info, slug):
    # Raise error if requested slug is already taken.
    product = models.Product.objects.filter(slug=slug).first()
    if product and product.company.user != info.context.user:
        msg = "This slug is already taken."
        code = ProductErrorCode.ALREADY_EXISTS.value
        raise ValidationError({"id": ValidationError(msg, code=code)})

