import graphene
from django.utils.crypto import get_random_string
from ...profile.types import Company
from ....core.permissions import ProductPermissions
from ....product import models
from ....product.error_codes import ProductErrorCode
from ...core.scalars import PositiveDecimal
from ...core.types import SeoInput
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ProductError
from ...product.types import Product, Category
from ...product.utils import product_permission
from ..utils import clean_product_slug
from ..enums import ProductUnitsEnum, DeliveryTimeOptionEnum
from ...core.utils import validate_slug_and_generate_if_needed
from django.core.exceptions import ValidationError


class ProductInput(graphene.InputObjectType):
    name = graphene.String(description="Product name.")
    slug = graphene.String(description="Product slug.")
    description_plaintext = graphene.String(description="Product Description plain text.")
    description = graphene.JSONString(description="Product content (JSON).")
    hs_code = graphene.String(description="Product HS code.")
    category = graphene.ID(description="Product category ID")
    unit_number = PositiveDecimal(description="Product unit number.")
    unit = ProductUnitsEnum(description="Product unit type.")
    quantity_unit = ProductUnitsEnum(description="Product quantity unit type.")
    unit_price = PositiveDecimal(description="Product unit price.")
    currency = graphene.String(description="Product unit price currency.")
    minimum_order_quantity = graphene.Int(description="Product minimum order quantity")
    organic = graphene.Boolean(description="Determines if product is organic.")
    private_label = graphene.Boolean(description="Determines if product private label is available.")
    seo = SeoInput(description="Search engine optimization fields.")
    is_published = graphene.Boolean(description="Determines if product is visible to customers.")
    is_brand = graphene.Boolean(description="Determines if product has brand.")
    brand = graphene.String(description="product brand.")
    rosetter = graphene.List(graphene.ID, description="List of rosetter of the product",)
    certificate_type = graphene.List(graphene.ID, description="List of certificate type of the product",)
    tags = graphene.List(graphene.String, description="product brand.")
    delivery_time_option = DeliveryTimeOptionEnum(description="product delivery time option.")
    delivery_time = graphene.String(description="product delivery time.")
    packaging = graphene.String(description="product delivery packaging description.")
    delivery = graphene.String(description="product delivery delivery description.")


class ProductCreate(ModelMutation):
    product = graphene.Field(
        Product, description="A created product."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add Product."
        )
        input = ProductInput(
            required=True, description="Fields required to create a product."
        )

    class Meta:
        description = "Creates a new product."
        model = models.Product
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        category = cls.get_node_or_error(
            info, data['category'], only_type=Category, field="category_id"
        )
        if category is None:
            raise ValidationError({"category": "This field cannot be blank."}, code=ProductErrorCode.REQUIRED)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "name", cleaned_input
            )
        except ValidationError as error:
            error.code = ProductErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        if not data['is_brand']:
            data['brand'] = None
        return cleaned_input

    @classmethod
    def get_instance(cls, info, company_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        instance = super().get_instance(info, **data)
        instance.user = info.context.user
        instance.company = company
        return instance

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()
        instance.rosetter.add(*cleaned_input["rosetter"])
        instance.certificate_type.add(*cleaned_input["certificate_type"])


class ProductActivate(ModelDeleteMutation):
    product = graphene.Field(
        Product, description="An activated product."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to activate."
        )

    class Meta:
        description = "Activates a product."
        model = models.Product
        # permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product.is_active = True
        product.save()
        return ProductActivate(product=product)


class ProductPublish(ModelMutation):
    product = graphene.Field(
        Product, description="A published product."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to be published."
        )

    class Meta:
        description = "Publishes a product."
        model = models.Product
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product.is_published = True
        product.save()
        return ProductPublish(product=product)


class ProductUpdate(ModelMutation):
    product = graphene.Field(Product, description="An updated product.")

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to update."
        )
        input = ProductInput(
            required=True, description="Fields required to update a product."
        )

    class Meta:
        description = "Updates an existing product."
        model = models.Product
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        cleaned_input = cls.clean_input(info, product, data.get("input"))
        product = cls.construct_instance(product, cleaned_input)
        cls.clean_instance(info, product)
        cls.save(info, product, cleaned_input)
        if "rosetter" in cleaned_input and cleaned_input["rosetter"]:
            product.rosetter.set(cleaned_input["rosetter"])
        if "certificate_type" in cleaned_input:
            product.certificate_type.set(cleaned_input["certificate_type"])
        return ProductUpdate(product=product)


class ProductUnpublish(ModelMutation):
    product = graphene.Field(
        Product, description="An unpublished product."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to be unpublished."
        )

    class Meta:
        description = "Unpublishes a product."
        model = models.Product
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product.is_published = False
        product.save()
        return ProductUnpublish(product=product)


class ProductDeactivate(ModelMutation):
    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to deactivate."
        )

    class Meta:
        description = "Deactivates a product."
        model = models.Product
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product.is_active = False
        product.is_published = False
        product.slug = product.slug + "-deactivated-" + get_random_string()
        product.save()
        return ProductDeactivate(product=product)


class ProductDelete(ModelDeleteMutation):
    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to delete."
        )

    class Meta:
        description = "Deletes a product."
        model = models.Product
        # permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = ProductError
        error_type_field = "product_errors"

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(
            info, product_id, only_type=Product, field="product_id"
        )
        product_permission(info, product)
        product.delete()
        return ProductDelete(product=product)
