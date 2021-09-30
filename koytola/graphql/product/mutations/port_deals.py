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
from ...account.i18n import I18nMixin
from ...account.types import Address, AddressInput
from ....core.utils import generate_unique_slug
from ...core.mutations import ModelBulkDeleteMutation, BaseBulkMutation
from ...product.types import PortDeals, PortProductGallery
from ...profile.types import Company
from ....core.permissions import ProductPermissions
from ...profile.utils import (company_permission, )
from ..enums import ProductUnitsEnum
import requests
import json
import urllib
from datetime import datetime


class PortDealsInput(graphene.InputObjectType):
    company_id = graphene.ID(description="Success Story Name")
    name = graphene.String(description="Success Story Title")
    address = AddressInput(description="Port Deals address of the account.")
    lat = graphene.Float(description="Port Deals address lat.")
    lng = graphene.Float(description="Port Deals address long.")
    product_name = graphene.String(description="Success Story Title")
    hs_code = graphene.String(description="Success Story Title")
    quantity = graphene.Int(description="Success Story Title")
    container_number = graphene.String(description="Port Deals container_number")
    unit = ProductUnitsEnum(description="Product unit type.")
    quantity_unit = ProductUnitsEnum(description="Product unit type.")
    price = graphene.Float(description="Success Story Title")
    currency = graphene.String(description="Product unit price currency.")
    start_date = graphene.DateTime(description="Success Story Title")
    end_date = graphene.DateTime(description="Success Story Company Name")
    discount_price = graphene.Float(description="Success Story Title")
    discount_percentage = graphene.Float(description="Success Story Title")
    certificate = graphene.List(graphene.String, description="Success Story Title")
    description = graphene.String(description="Success Story Title")
    is_active = graphene.Boolean(description="")


class PortDealsUpdateInput(graphene.InputObjectType):
    company_id = graphene.ID(description="Port Deals address ompany id")
    name = graphene.String(description="Port Deals Title")
    address = AddressInput(description="Port Deals address of the account.")
    address_id = graphene.ID(description="Port Deals address id")
    lat = graphene.Float(description="Port Deals address lat.")
    lng = graphene.Float(description="Port Deals address long.")
    product_name = graphene.String(description="Success Story Title")
    hs_code = graphene.String(description="Success Story Title")
    quantity = graphene.Int(description="Success Story Title")
    quantity_unit = ProductUnitsEnum(description="Product unit type.")
    container_number = graphene.String(description="Port Deals container number")
    unit = ProductUnitsEnum(description="Product unit type.")
    price = graphene.Float(description="Success Story Title")
    currency = graphene.String(description="Product unit price currency.")
    start_date = graphene.DateTime(description="Success Story Title")
    end_date = graphene.DateTime(description="Success Story Company Name")
    discount_price = graphene.Float(description="Success Story Title")
    discount_percentage = graphene.Float(description="Success Story Title")
    certificate = graphene.List(graphene.String, description="Success Story Title")
    description = graphene.String(description="Success Story Title")
    is_active = graphene.Boolean(description="")


class PortProductGalleryInput(graphene.InputObjectType):
    image = Upload(description="Success Story Title", required=False)
    video = Upload(description="Success Story Title", required=False)
    alt_text = graphene.String(description="Success Story Title")
    is_active = graphene.Boolean(description="")


class PortDealsCreate(ModelMutation, I18nMixin):
    PortDeals = graphene.Field(PortDeals, description="A created social responsibility.")

    class Arguments:
        input = PortDealsInput(required=True, description="Fields required to create a offer.")

    class Meta:
        description = "Creates a new social responsibility."
        model = models.PortDeals
        error_type_class = ProductError
        error_type_field = "deals_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(instance, "name", cleaned_input)
        except ValidationError as error:
            error.code = ProductErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        return cleaned_input

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        company = cls.get_node_or_error(info, data['input']['company_id'], only_type=Company, field="company_id")
        company_permission(info, company)
        instance.company = company

        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        address_cleaned_input = data["input"]["address"]
        address = cls.validate_address(address_cleaned_input)
        cls.clean_instance(info, address)
        cls.save(info, address, address_cleaned_input)
        cls._save_m2m(info, address, address_cleaned_input)
        instance.address = address
        cleaned_input.pop("address")

        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return PortDealsCreate(PortDeals=instance)

    @classmethod
    def get_type_for_model(cls):
        return PortDeals


class PortDealsUpdate(ModelMutation, I18nMixin):
    PortDeals = graphene.Field(PortDeals, description="An updated offer.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a company to update.")
        input = PortDealsUpdateInput(required=True, description="Fields required to update a offer.")

    class Meta:
        description = "Updates an existing Offer."
        model = models.PortDeals
        error_type_class = ProductError
        error_type_field = "deals_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(instance, "name", cleaned_input)
        except ValidationError as error:
            error.code = ProductErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        return cleaned_input

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        port_deal = cls.get_node_or_error(info, id, only_type=PortDeals, field="id")
        cleaned_input = cls.clean_input(info, port_deal, data.get("input"))

        address_id = data["input"]["address_id"]
        data["input"].pop("address_id")
        address_cleaned_input = data["input"]["address"]
        address = cls.get_node_or_error(info, address_id, only_type=Address, field="id")
        address = cls.construct_instance(address, address_cleaned_input)
        cls.clean_instance(info, address)
        cls.save(info, address, address_cleaned_input)
        port_deal.address = address
        cleaned_input.pop("address")
        if cleaned_input['end_date'] <= datetime.now():
            if not port_deal.is_expire:
                port_deal.is_expire = True
        port_deal = cls.construct_instance(port_deal, cleaned_input)
        cls.clean_instance(info, port_deal)
        cls.save(info, port_deal, cleaned_input)
        return PortDealsUpdate(PortDeals=port_deal)


class PortDealsGalleryCreate(ModelMutation):
    port_deals_gallery = graphene.Field(PortProductGallery, description="A created product video.")

    class Arguments:
        port_deal_id = graphene.ID(required=True, description="ID of a product to add product video.")
        input = PortProductGalleryInput(required=False, description="Fields required to create a product video.")

    class Meta:
        description = "Creates a new product video."
        model = models.PortProductGallery
        error_type_class = ProductError
        error_type_field = "deals_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, port_deal_id, **data):
        port_deal = cls.get_node_or_error(info, port_deal_id, only_type=PortDeals, field="port_deal_id")
        port_deals_gallery = models.PortProductGallery.objects.create(product=port_deal)
        cleaned_input = cls.clean_input(info, port_deals_gallery, data.get("input"))
        port_deals_gallery = cls.construct_instance(port_deals_gallery, cleaned_input)
        cls.clean_instance(info, port_deals_gallery)
        cls.save(info, port_deals_gallery, cleaned_input)
        return PortDealsGalleryCreate(port_deals_gallery=port_deals_gallery)


class PortDealsGalleryDelete(ModelDeleteMutation):
    port_deals_gallery = graphene.Field(PortProductGallery, description="A delete Port Deals Gallery.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of a product to activate.")

    class Meta:
        description = "Delete an existing Port Deals Gallery."
        model = models.PortProductGallery
        error_type_class = ProductError
        error_type_field = "deals_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        port_deals_gallery = cls.get_node_or_error(info, id, only_type=PortProductGallery, field="offer_id")
        port_deals_gallery.delete()
        return PortDealsGalleryDelete()


class PortDealsBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(graphene.ID, required=True, description="List of company Port Deals to delete.")

    class Meta:
        description = "Deactivate an existing Port Deals."
        model = models.PortDeals
        error_type_class = ProductError
        error_type_field = "deals_errors"
