import graphene
from ....product import models, emails
from ...core.mutations import ModelMutation
from ...core.types.common import ProductError
from ...product.types import Product, ProductQuery
from ...account.enums import CountryCodeEnum


class ProductQueryInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="Order user name .")
    email = graphene.String(required=True, description="Order user name .")
    offer = graphene.ID(required=False,  description="Product offer.")
    quantity = graphene.Int(required=True, description="Product quantity.")
    message = graphene.String(required=True, description="Product message.")
    country = CountryCodeEnum(description="Country.")


class ProductQueryCreate(ModelMutation):
    productQuery = graphene.Field(
        ProductQuery, description="A created product Query."
    )

    class Arguments:
        product_id = graphene.ID(
            required=True, description="ID of a product to add product Query."
        )
        input = ProductQueryInput(
            required=True, description="Fields required to create a product Query."
        )

    class Meta:
        description = "Creates a new product Query."
        model = models.ProductQuery
        error_type_class = ProductError
        error_type_field = "product_errors"

    # @classmethod
    # def check_permissions(cls, context):
    #     return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, product_id, **data):
        product = cls.get_node_or_error(info, product_id, only_type=Product, field="product_id")
        product_query = models.ProductQuery.objects.create(product=product)
        cleaned_input = cls.clean_input(info, product_query, data.get("input"))
        product_query = cls.construct_instance(product_query, cleaned_input)
        cls.clean_instance(info, product_query)
        cls.save(info, product_query, cleaned_input)
        emails.send_confirm_order_mail_("order/buyer", cleaned_input['email'], product_query)
        emails.send_confirm_order_mail_("order/seller", product_query.product.company.user.email, product_query)
        return ProductQueryCreate(productQuery=product_query)
