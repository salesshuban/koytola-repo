import graphene
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from ..enums import ProfileCompanyType
from ....core.permissions import ProfilePermissions
from ....profile import models
from ....profile.error_codes import ProfileErrorCode
from ...account.i18n import I18nMixin
from ...account.types import Address, AddressInput, User
from ...core.types import SeoInput, Upload
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import AccountError, ProfileError
from ...core.utils import (
    clean_seo_fields,
    update_publication_date,
    validate_image_file,
    validate_slug_and_generate_if_needed,
    validate_slug_value,
)
from ...account.enums import CountryCodeEnum
from ...profile.types import Company, Industry
from ....profile.thumbnails import (
    create_company_logo_thumbnails
)
from ..utils import (
    clean_company_slug,
    company_address_permission,
    company_permission,
)


class CompanyInput(graphene.InputObjectType):
    industry = graphene.String(description="Company industry", required=False)
    name = graphene.String(description="Company name.")
    slug = graphene.String(description="Company username slug.")
    logo = Upload(description="Company logo file.")
    logo_alt = graphene.String(description="Alt text for your Company logo.")
    address = AddressInput(description="Billing address of the account.")
    founded_year = graphene.Int(description="Company founded year.")
    no_of_employees = graphene.String(description="Company number of employees.")
    content_plaintext = graphene.String(description="Company content plaintext.")
    vision = graphene.String(description="Company vision.")
    content = graphene.JSONString(description="Company content (JSON).")
    website = graphene.String(description="Company Url.")
    # email = graphene.String(description="Company contact email address.")
    phone = graphene.String(description="Company phone.")
    export_countries = graphene.List(
        CountryCodeEnum,
        description="Export countries' codes of the company.",
    )
    is_brand = graphene.Boolean(description="Company brands will create if value is true.")
    brands = graphene.List(graphene.String, description="List of brands of the company",)
    membership = graphene.List(graphene.String, description="List of membership of the company",)
    rosetter = graphene.List(graphene.ID, description="List of rosetter of the company",)
    organic_products = graphene.Boolean(description="organic products is available if value is true.")
    private_label = graphene.Boolean(description="private labeling is available if value is true.")
    female_leadership = graphene.Boolean(description="female leadership is available if value is true.")
    is_published = graphene.Boolean(description="Determines if product is visible to customers.")
    publication_date = graphene.String(description="Publication date. ISO 8601 standard.")
    seo = SeoInput(description="Search engine optimization fields.")
    type = ProfileCompanyType(description="Company type")


class CompanyInputAdmin(CompanyInput):
    user = graphene.ID(description="ID of the profile's owner.", name="user")


class CompanyCreate(ModelMutation):
    company = graphene.Field(
        Company, description="A created company."
    )

    class Arguments:

        input = CompanyInput(
            required=True, description="Fields required to create a company."
        )

    class Meta:
        description = "Creates a new company."
        model = models.Company
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        company_permission(info, instance)
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(
                instance, "name", cleaned_input
            )
        except ValidationError as error:
            error.code = ProfileErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input)
        return cleaned_input

    @classmethod
    def get_instance(cls, info, **data):
        instance = super().get_instance(info, **data)
        instance.user = info.context.user
        return instance

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()


class CompanyActivate(ModelDeleteMutation):
    company = graphene.Field(
        Company, description="An activated company."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to activate."
        )

    class Meta:
        description = "Activates a company."
        model = models.Company
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        company.is_active = True
        company.save()
        return CompanyActivate(company=company)


class CompanyPublish(ModelMutation):
    profile = graphene.Field(
        Company, description="A published company."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to be published."
        )

    class Meta:
        description = "Publishes a company."
        model = models.Company
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        company.is_published = True
        company.save()
        return CompanyPublish(company=company)


class CompanyUpdate(ModelMutation):
    company = graphene.Field(Company, description="An updated company.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to update."
        )

        input = CompanyInput(
            required=True, description="Fields required to update a company."
        )

    class Meta:
        description = "Updates an existing company."
        model = models.Company
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        try:
            cleaned_input = validate_slug_and_generate_if_needed(instance, "name", cleaned_input)
        except ValidationError as error:
            error.code = ProfileErrorCode.REQUIRED
            raise ValidationError({"slug": error})
        if data.get("logo"):
            image_data = info.context.FILES.get(data["logo"])
            validate_image_file(image_data, "logo")
        if 'is_brand' not in cleaned_input or not cleaned_input['is_brand']:
            cleaned_input['brands'] = ""
        clean_seo_fields(cleaned_input)
        update_publication_date(cleaned_input)
        return cleaned_input

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        clean_company_slug(info, data)
        cleaned_input = cls.clean_input(info, company, data.get("input"))
        if 'industry' in cleaned_input and cleaned_input['industry']:
            cleaned_input['industry'] = cls.get_node_or_error(
                info, cleaned_input['industry'], only_type=Industry, field="id"
            )
        else:
            if 'industry' in cleaned_input:
                cleaned_input.pop('industry')
        if data.get("logo"):
            if company.logo:
                company.logo.delete_sized_images()
                company.logo.delete()
            create_company_logo_thumbnails.delay(company.pk)
        company = cls.construct_instance(company, cleaned_input)
        cls.clean_instance(info, company)
        cls.save(info, company, cleaned_input)
        if "rosetter" in cleaned_input and cleaned_input["rosetter"]:
            company.rosetter.set(cleaned_input["rosetter"])
        return CompanyUpdate(company=company)


class CompanyUpdateAdmin(ModelMutation):
    profile = graphene.Field(Company, description="An updated profile.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a profile to update."
        )
        input = CompanyInputAdmin(
            required=True, description="Fields required to update a profile as admin."
        )

    class Meta:
        description = "Updates an existing company profile as Admin."
        model = models.Company
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        data = data.get("input")
        if 'industry' in data and data['industry']:
            data['industry'] = cls.get_node_or_error(
                    info, data.get("industry"), only_type=Industry, field="industry_id"
                )
        else:
            if 'industry' in data:
                data.pop('industry')
        if "logo" not in data:
            update_publication_date(data, company)
        if "user" in data and data['user']:
            company.user = cls.get_node_or_error(info, data.get("user"), only_type=User, field="user_id")
        else:
            if 'user' in data:
                data.pop('user')
        cleaned_input = cls.clean_input(info, company, data)
        if data.get("logo"):
            if company.logo:
                company.logo.delete_sized_images()
                company.logo.delete()
            create_company_logo_thumbnails.delay(company.pk)
        company = cls.construct_instance(company, cleaned_input)
        cls.clean_instance(info, company)
        cls.save(info, company, cleaned_input)
        if "rosetter" in cleaned_input and cleaned_input["rosetter"]:
            company.rosetter.set(cleaned_input["rosetter"])
        return CompanyUpdateAdmin(company=company)

    @classmethod
    def get_type_for_model(cls):
        return Company


class CompanyUnpublish(ModelMutation):
    company = graphene.Field(
        Company, description="An unpublished company."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to be unpublished."
        )

    class Meta:
        description = "Unpublishes a company."
        model = models.Company
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        company.is_published = False
        company.save()
        return CompanyUnpublish(company=company)


class CompanyDeactivate(ModelMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to deactivate."
        )

    class Meta:
        description = "Deactivates a company profile."
        model = models.Company
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        company.is_active = False
        company.is_published = False
        company.slug = company.slug + "-deactivated-" + get_random_string()
        company.save()
        return CompanyDeactivate(company=company)


class CompanyDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a company to delete."
        )

    class Meta:
        description = "Deletes a company profile."
        model = models.Company
        permissions = (ProfilePermissions.MANAGE_PROFILES,)
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        company = cls.get_node_or_error(
            info, id, only_type=Company, field="id"
        )
        company_permission(info, company)
        company.delete()
        return CompanyDelete(company=company)


class CompanyAddressCreate(ModelMutation, I18nMixin):
    company = graphene.Field(
        Company, description="A company profile for which the address was created."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to create address for."
        )
        input = AddressInput(
            description="Fields required to create address.", required=True
        )

    class Meta:
        description = "Create an address for the company."
        model = models.Address
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, company_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        company_permission(info, company)
        cleaned_input = cls.clean_input(
            info=info, instance=Address(), data=data.get("input")
        )
        address = cls.validate_address(cleaned_input)
        cls.clean_instance(info, address)
        cls.save(info, address, cleaned_input)
        cls._save_m2m(info, address, cleaned_input)
        company.address = address
        company.save()
        return CompanyAddressCreate(company=company)

    @classmethod
    def save(cls, info, instance, cleaned_input):
        super().save(info, instance, cleaned_input)
        user = info.context.user
        instance.user_addresses.add(user)


class CompanyAddressUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of the address to be updated."
        )
        input = AddressInput(
            description="Fields required to create address.", required=True
        )

    class Meta:
        description = "Updates an address of the company."
        model = models.Address
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        address = cls.get_node_or_error(
            info, id, only_type=Address, field="id"
        )
        company_address_permission(info, address)
        cleaned_input = cls.clean_input(info, address, data.get("input"))
        address = cls.construct_instance(address, cleaned_input)
        cls.clean_instance(info, address)
        cls.save(info, address, cleaned_input)
        return CompanyAddressUpdate()


class CompanyAddressDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of the company address to be deleted."
        )

    class Meta:
        description = "Deletes an address of the company."
        model = models.Address
        error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        address = cls.get_node_or_error(
            info, id, only_type=Address, field="id"
        )
        company_address_permission(info, address)
        address.delete()
        return CompanyAddressDelete()
