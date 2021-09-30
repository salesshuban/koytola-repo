import graphene
from graphene import relay
from graphene_federation import key
from ..core.scalars import Array
from ...profile import models
from ..core.connection import CountableDjangoObjectType
from ..core.types import Image
from ..core.types.common import BrochureFile
from ..core.types import CountryDisplay
from ..product.types import Product, Category
from .dataloaders import (
    CompanyByIdLoader,
)
from .enums import MessageStatusEnum, MessageTypeEnum
from ..core.types.rosetters import Roetter
from ..core.types.certificate_type import CertificateType


class Representative(CountableDjangoObjectType):
    photo = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Sizes of the representative photo.")
    )
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that representative belongs to.",
        ),
    )

    class Meta:
        description = (
            "Company Representative."
        )
        only_fields = [
            "id",
            "linkedin_url",
            "name",
            "photo",
            "photo_alt",
            "position",
        ]
        interfaces = [relay.Node]
        model = models.Representative

    @staticmethod
    def resolve_photo(root: models.Representative, info, size=None, **_kwargs):
        if root.photo:
            return Image.get_adjusted(
                image=root.photo,
                alt=root.photo_alt,
                size=size,
                rendition_key_set="representative_photos",
                info=info,
            )

    @staticmethod
    def resolve_company(root: models.Representative, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None


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


@key("id")
class Brochure(CountableDjangoObjectType):
    brochure = graphene.String(description="Company brochure url.")
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that brochure belongs to.",
        ),
    )

    class Meta:
        description = (
            "Company brochures."
        )
        only_fields = [
            "id",
            "description",
            "name",
            "sort_order",
        ]
        interfaces = [relay.Node]
        model = models.Brochure

    @staticmethod
    def resolve_brochure(root: models.Brochure, info):
        brochure = root.brochure
        if not brochure:
            return None
        return info.context.build_absolute_uri(brochure.url)

    @staticmethod
    def resolve_company(root: models.Brochure, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None


@key("id")
class Images(CountableDjangoObjectType):
    image = graphene.Field(Image, size=graphene.Int(description="Size of the image."))
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that Image belongs to.",
        ),
    )

    class Meta:
        description = (
            "Company images."
        )
        only_fields = [
            "id",
            "description",
            "name",
            "sort_order",
        ]
        interfaces = [relay.Node]
        model = models.Images

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

    @staticmethod
    def resolve_company(root: models.Images, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None


@key("id")
class Video(CountableDjangoObjectType):
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that video belongs to.",
        ),
    )
    video = graphene.String(description="Company video url.")

    class Meta:
        description = (
            "Company videos."
        )
        only_fields = [
            "id",
            "description",
            "name",
            "sort_order",
            "youtube_url",
        ]
        interfaces = [relay.Node]
        model = models.Video

    @staticmethod
    def resolve_company(root: models.Video, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None

    @staticmethod
    def resolve_video(root: models.Video, info):
        video = root.video
        if not video:
            return None
        return info.context.build_absolute_uri(video.url)


@key("id")
class SocialResponsibility(CountableDjangoObjectType):
    brochure = graphene.Field(
        lambda: BrochureFile,
        description="Company social responsibility brochure url."
    )
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that social responsibility belongs to.",
        ),
    )
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Company social responsibility image sizes.")
    )
    video = graphene.String(
        description="Company social responsibility video url."
    )

    class Meta:
        description = (
            "Company social responsibilities."
        )
        only_fields = [
            "id",
            "description",
            "name",
            "sort_order",
            "youtube_url",
            "brochure_file_name",
            "created_at",
        ]
        interfaces = [relay.Node]
        model = models.SocialResponsibility

    @staticmethod
    def resolve_brochure(root: models.SocialResponsibility, info):
        if root.brochure.name:
            return root.brochure
        else:
            return None

    @staticmethod
    def resolve_company(root: models.SocialResponsibility, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None

    @staticmethod
    def resolve_image(root: models.SocialResponsibility, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.description,
                size=size,
                rendition_key_set="images",
                info=info,
            )

    @staticmethod
    def resolve_video(root: models.SocialResponsibility, info):
        video = root.video
        if not video:
            return None
        return info.context.build_absolute_uri(video.url)


@key("id")
class Contact(CountableDjangoObjectType):
    status = MessageStatusEnum(description="Company contact status.")
    type = MessageTypeEnum(description="Company contact type.")
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that video belongs to.",
        ),
    )

    class Meta:
        description = (
            "Company contact messages."
        )
        only_fields = [
            "id",
            "name",
            "email",
            "country",
            "submission_date",
            "ask_for_reference",
            "subject",
            "contact",
        ]
        interfaces = [relay.Node]
        model = models.Contact

    @staticmethod
    def resolve_company(root: models.SocialResponsibility, info, **_kwargs):
        if root.company_id:
            return CompanyByIdLoader(info.context).load(root.company_id)
        return None


# @key("id")
class Industry(CountableDjangoObjectType):
    name = graphene.String(description="Company Industry.")
    is_active = graphene.Boolean(description="Company contact type.")
    children = graphene.List(
        lambda: Industry, description="List of children of the category."
    )

    class Meta:
        description = ("Company Industry list.", )
        only_fields = ["id", "name", "is_active"]
        interfaces = [relay.Node]
        model = models.Industry

    @staticmethod
    def resolve_children(root: models.Industry, info, **_kwargs):
        return root.children.all()


@key("id")
@key("slug")
class SuccessStory(CountableDjangoObjectType):
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Success Story image sizes.")
    )
    tags = Array()
    
    class Meta:
        description = (
            "Success Story."
        )
        only_fields = [
            "title",
            "name",
            "description",
            "location",
            "company_name",
            "slug",
            "created_at",
            "is_active",
            "tags"
        ]
        interfaces = [relay.Node]
        model = models.SuccessStory

    @staticmethod
    def resolve_tags(root: models.SocialResponsibility, info, size=None, **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_image(root: models.SocialResponsibility, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.description,
                size=size,
                rendition_key_set="images",
                info=info,
            )


class TradeShow(CountableDjangoObjectType):
    company = graphene.Field(
        "koytola.graphql.profile.types.Company",
        description=(
            "Company that video belongs to.",
        ),
    )
    
    class Meta:
        description = (
            "Success Story."
        )
        only_fields = [
            "name",
            "year",
            "city",
            "created_at",
            "updated_at"
        ]
        interfaces = [relay.Node]
        model = models.TradeShow
    
    
@key("id")
@key("slug")
class Company(CountableDjangoObjectType):
    logo = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Sizes of the company logo.")
    )
    representative = graphene.Field(
        lambda: Representative,
        description="Company representative."
    )
    industry = graphene.Field(
        lambda: Industry,
        description="Company Industry."
    )
    certificates = graphene.List(
        lambda: Certificate,
        description="List of company certificates."
    )
    brochures = graphene.List(
        lambda: Brochure,
        description="List of company brochures."
    )
    videos = graphene.List(
        lambda: Video,
        description="List of company videos."
    )
    trade_show = graphene.List(
        lambda: TradeShow,
        description="List of company Trade Show."
    )
    social_responsibilities = graphene.List(
        lambda: SocialResponsibility,
        description="List of company social responsibilities."
    )
    categories = graphene.List(
        lambda: Category,
        description="Company product categories."
    )
    products = graphene.List(
        lambda: Product,
        description="Company products."
    )
    no_of_employees = graphene.String(description="Company number of employees.")
    export_countries = graphene.List(
        CountryDisplay,
        description="List of countries available for the shipping voucher.",
    )
    brands = Array(description="Company brands")
    rosetter = graphene.List(lambda: Roetter, description="Company rosetter")
    membership = Array(description="Company membership")

    class Meta:
        description = (
            "Company profile."
        )
        only_fields = [
            "id",
            "user",
            "slug",
            "name",
            "seo_title",
            "seo_description",
            "logo",
            "logo_alt",
            "website",
            "address",
            "founded_year",
            "type",
            "no_of_employees",
            # "email",
            "content",
            "is_active",
            "is_verified",
            "creation_date",
            "publication_date",
            "update_date",
            "is_published",
            "is_brand",
            "organic_products",
            "private_label",
            "female_leadership",
            "branded_value",
        ]
        interfaces = [relay.Node]
        model = models.Company

    @staticmethod
    def resolve_brands(root: models.Company, info, size=None, **_kwargs):
        if root.brands:
            return eval(root.brands)
        else:
            return []

    @staticmethod
    def resolve_membership(root: models.Company, info, size=None, **_kwargs):
        if root.membership:
            return eval(root.membership)
        else:
            return []

    @staticmethod
    def resolve_rosetter(root: models.Company, info, size=None, **_kwargs):
        return root.rosetter.all()

    @staticmethod
    def resolve_trade_show(root: models.Company, info, size=None, **_kwargs):
        return root.company_trade_show.all()

    @staticmethod
    def resolve_logo(root: models.Company, info, size=None, **_kwargs):
        if root.logo:
            return Image.get_adjusted(
                image=root.logo,
                alt=root.logo_alt,
                size=size,
                rendition_key_set="company_logos",
                info=info,
            )

    @staticmethod
    def resolve_representative(root: models.Company, info, **_kwargs):
        return root.representative.first()

    @staticmethod
    def resolve_industry(root: models.Company, info, **_kwargs):
        return root.industry

    @staticmethod
    def resolve_certificates(root: models.Company, info, **_kwargs):
        return root.certificates.all()

    @staticmethod
    def resolve_brochures(root: models.Company, info, **_kwargs):
        return root.brochures.all()

    @staticmethod
    def resolve_videos(root: models.Company, info, **_kwargs):
        return root.videos.all()

    @staticmethod
    def resolve_social_responsibilities(root: models.Company, info, **_kwargs):
        return root.social_responsibilities.all()

    @staticmethod
    def resolve_categories(root: models.Company, info, **_kwargs):
        products = root.products.published()
        categories = []
        for product in products:
            if product not in categories:
                categories.append(product.category)
        return list(set(categories))

    @staticmethod
    def resolve_products(root: models.Company, info, **_kwargs):
        return root.products.published()

    @staticmethod
    def resolve_export_countries(root: models.Company, info, **_kwargs):
        return [
            CountryDisplay(code=country.code, country=country.name)
            for country in root.export_countries
        ]
