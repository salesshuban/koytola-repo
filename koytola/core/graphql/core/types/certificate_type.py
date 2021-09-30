from ..connection import CountableDjangoObjectType
import graphene
from graphene import relay
from ....profile import models
from ...core.types import Image
from ...profile.dataloaders import (
    CompanyByIdLoader,
)


class CertificateType(CountableDjangoObjectType):
    name = graphene.String(description="Certificate Type Name.")
    description = graphene.String(description="Certificate Type description.")
    is_active = graphene.Boolean(description="Certificate Type Activity.")
    image = graphene.Field(Image, size=graphene.Int(description="Size of the image."))

    class Meta:
        description = ("Certificate Type list.", )
        only_fields = ["id", "name", "type", "description", "is_active", "image", "creation_date", "update_date"]
        interfaces = [relay.Node]
        model = models.CertificateType

    @staticmethod
    def resolve_image(root: models.Images, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=None,
                size=size,
                rendition_key_set="user_avatars",
                info=info,
            )


class Certificate(CountableDjangoObjectType):
    certificate = graphene.String(description="Company certificate url.")
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that certificate belongs to.",
        ),
    )

    type = graphene.Field(
        lambda: CertificateType,
        description="Certificate Type."
    )

    class Meta:
        description = (
            "Company certificates."
        )
        only_fields = [
            "id",
            "description",
            "name",
            "sort_order",
        ]
        interfaces = [relay.Node]
        model = models.Certificate


    @staticmethod
    def resolve_type(root: models.Certificate, info, **_kwargs):
        return root.type

    @staticmethod
    def resolve_certificate(root: models.Certificate, info):
        certificate = root.certificate
        if not certificate:
            return None
        return info.context.build_absolute_uri(certificate.url)

    @staticmethod
    def resolve_company(root: models.Certificate, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None

