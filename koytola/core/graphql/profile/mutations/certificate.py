import graphene

from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, Certificate, CertificateType
from ..utils import company_permission


class CertificateInput(graphene.InputObjectType):
    certificate = Upload(description=" Company certificate file.", required=False)
    sort_order = graphene.Int(description="The order of your certificate.")
    

class CertificateCreate(ModelMutation):
    certificate = graphene.Field(
        Certificate, description="A created certificate."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add certificate."
        )
        certificate_type_id = graphene.ID(
            required=True, description="ID of a company to add certificate."
        )
        input = CertificateInput(
            required=True, description="Fields required to create a certificate."
        )

    class Meta:
        description = "Creates a new certificate."
        model = models.Certificate
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, company_id, certificate_type_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        company_permission(info, company)
        instance = cls.get_instance(info, **data)
        instance.company = company
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        cleaned_input['type'] = cls.get_node_or_error(
            info, certificate_type_id, only_type=CertificateType, field="certificate_type_id"
        )
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return CertificateCreate(certificate=instance)

    @classmethod
    def get_type_for_model(cls):
        return Certificate


class CertificateUpdate(ModelMutation):
    certificate = graphene.Field(Certificate, description="An updated certificate.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a certificate to update."
        )
        input = CertificateInput(
            required=True, description="Fields required to update a certificate."
        )

    class Meta:
        description = "Updates an existing certificate."
        model = models.Certificate
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        certificate = cls.get_node_or_error(
            info, id, only_type=Certificate, field="id"
        )
        company_permission(info, certificate.company)
        cleaned_input = cls.clean_input(info, certificate, data.get("input"))
        contact = cls.construct_instance(certificate, cleaned_input)
        cls.clean_instance(info, contact)
        cls.save(info, contact, cleaned_input)
        return CertificateUpdate(certificate=certificate)

    @classmethod
    def get_type_for_model(cls):
        return Certificate


class CertificateDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a certificate to delete."
        )

    class Meta:
        description = "Deletes a certificate."
        model = models.Certificate
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        certificate = cls.get_node_or_error(
            info, id, only_type=Certificate, field="id"
        )
        company_permission(info, certificate.company)
        certificate.delete()
        return CertificateDelete(certificate=certificate)
