import graphene
from django.core.exceptions import ValidationError
from ....product import models
from ....product.error_codes import ProductErrorCode
from ...core.types import Upload
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ProfileError, ProductError
from ...core.utils import (
    validate_slug_and_generate_if_needed
)
from ....core.utils import generate_unique_slug
from ...core.mutations import ModelBulkDeleteMutation, BaseBulkMutation
from ...product.types import Offers, Product, Category
from ...profile.types import Company
from ....core.permissions import ProductPermissions
from ...profile.utils import (company_permission,)
from ...core.scalars import PositiveDecimal


class OffersInput(graphene.InputObjectType):
    company_id = graphene.ID(description="Success Story Name")
    title = graphene.String(description="Success Story Title")
    get_code = graphene.String(description="Success Story Name")
    value = PositiveDecimal(description="Product unit price.")
    unit = graphene.String(description="Success Story Description")
    image = Upload(description="Success Story file.")
    start_date = graphene.DateTime(description="Success Story Title")
    end_date = graphene.DateTime(description="Success Story Company Name")
    tags = graphene.List(graphene.String, description="Success Story tags")
    apply_on = graphene.String(description="Success Story Description")
    products = graphene.List(graphene.ID, description="Success Story tags")
    categories = graphene.List(graphene.ID, description="Success Story tags")
    all_product = graphene.Boolean(description="Success Story all product")
    all_category = graphene.Boolean(description="Success Story all product")
    total_cart = graphene.Boolean(description="Success Story tags")
    min_cart_value = graphene.Int(description="Success Story tags")
    is_active = graphene.Boolean(description="Success Story tags")


class OffersCreate(ModelMutation):
    Offer = graphene.Field(Offers, description="A created social responsibility.")

    class Arguments:
        input = OffersInput(required=True, description="Fields required to create a offer.")

    class Meta:
        description = "Creates a new social responsibility."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        if info.context.user.is_superuser:
            instance.user = info.context.user
        return instance

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        all_product, all_category = data['input']['all_product'], data['input']['all_category']
        data['input'].pop('all_product')
        data['input'].pop('all_category')
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        if not info.context.user.is_superuser:
            company = cls.get_node_or_error(info, data['input']['company_id'], only_type=Company, field="company_id")
            company_permission(info, company)
            instance.company = company
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        if all_category:
            instance.categories.add(*models.Category.objects.filter(parent=None))
        else:
            if 'categories' in cleaned_input and cleaned_input['categories']:
                instance.categories.add(*cleaned_input['categories'])
        if all_product:
            instance.products.add(*models.Product.objects.filter(company=instance.company))
        else:
            if 'products' in cleaned_input and cleaned_input['products']:
                instance.products.add(*cleaned_input['products'])
        return OffersCreate(Offer=instance)

    @classmethod
    def get_type_for_model(cls):
        return Offers


class OffersUpdate(ModelMutation):
    Offer = graphene.Field(Offers, description="An updated offer.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a company to update.")
        input = OffersInput(required=True, description="Fields required to update a offer.")

    class Meta:
        description = "Updates an existing Offer."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        if not cleaned_input['image']:
            cleaned_input.pop('image')
        if 'title' in cleaned_input:
            cleaned_input['slug'] = generate_unique_slug(instance, cleaned_input['title'])
        return cleaned_input

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        offer = cls.get_node_or_error(info, id, only_type=Offers, field="id")
        all_product, all_category = data['input']['all_product'], data['input']['all_category']
        data['input'].pop('all_product')
        data['input'].pop('all_category')
        cleaned_input = cls.clean_input(info, offer, data.get("input"))
        offer = cls.construct_instance(offer, cleaned_input)
        cls.clean_instance(info, offer)
        cls.save(info, offer, cleaned_input)
        if all_category:
            offer.categories.set(*models.Category.objects.filter(parent=None))
        else:
            if 'categories' in cleaned_input and cleaned_input['categories']:
                offer.categories.set(cleaned_input['categories'])
        if all_product:
            offer.products.set(models.Product.objects.filter(company=offer.company))
        else:
            if 'products' in cleaned_input and cleaned_input['products']:
                offer.products.set(cleaned_input['products'])
        return OffersUpdate(Offer=offer)


class OfferActivate(ModelDeleteMutation):
    Offer = graphene.Field(Offers, description="An updated offer.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Active an existing Offer."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        offer = cls.get_node_or_error(info, id, only_type=Offers, field="offer_id")
        offer.is_active = True
        offer.save()
        return OfferActivate(Offer=offer)


class OfferDeactivate(ModelDeleteMutation):
    Offer = graphene.Field(Offers, description="An updated offer.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Deactivate an existing Offer."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        offer = cls.get_node_or_error(info, id, only_type=Offers, field="offer_id")
        offer.is_active = False
        offer.save()
        return OfferDeactivate(Offer=offer)


class OfferDelete(ModelDeleteMutation):
    Offer = graphene.Field(Offers, description="An updated offer.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Deactivate an existing Offer."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        offer = cls.get_node_or_error(info, id, only_type=Offers, field="offer_id")
        offer.delete()
        return OfferDeactivate()


class OffersBulkDelete(ModelBulkDeleteMutation):

    class Arguments:
        ids = graphene.List(graphene.ID, required=True, description="List of company products to delete.")

    class Meta:
        description = "Deactivate an existing Offer."
        model = models.Offers
        error_type_class = ProductError
        error_type_field = "offer_errors"
