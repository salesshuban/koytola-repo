import graphene
from ....core.templatetags.images import get_thumbnail
from ...translations.enums import LanguageCodeEnum
from ..enums import (
    AccountErrorCode,
    AnalyticsErrorCode,
    AppErrorCode,
    BlogErrorCode,
    HelpdeskErrorCode,
    InvoiceErrorCode,
    JobStatusEnum,
    MenuErrorCode,
    MetadataErrorCode,
    NewsErrorCode,
    OrderErrorCode,
    PageErrorCode,
    PaymentErrorCode,
    PermissionEnum,
    PermissionGroupErrorCode,
    ProfileErrorCode,
    ProductErrorCode,
    PluginErrorCode,
    SiteErrorCode,
    WebhookErrorCode,
    TranslationErrorCode,
)
from .money import VAT
from ....account import models


class Image(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the image.")
    alt = graphene.String(description="Alt text for an image.")

    class Meta:
        description = "Represents an image."

    @staticmethod
    def get_adjusted(image, alt, size, rendition_key_set, info):
        """Return Image adjusted with given size."""
        if size:
            url = get_thumbnail(
                image_file=image,
                size=size,
                method="thumbnail",
                rendition_key_set=rendition_key_set,
            )
        else:
            url = image.url
        url = info.context.build_absolute_uri(url)
        return Image(url, alt)


class CountryDisplay(graphene.ObjectType):
    code = graphene.String(description="Country code.", required=True)
    country = graphene.String(description="Country name.", required=True)
    vat = graphene.Field(VAT, description="Country tax.")
    latitude = graphene.Float(description="Country latitude.", required=True)
    longitude = graphene.Float(description="Country longitude.", required=True)
    flag = graphene.Field(Image, size=graphene.Int(description="Size of the image."))

    def resolve_flag(self, info, size=None, **_kwargs):
        if models.Countries.objects.filter(code=self.code).first().flag:
            return Image.get_adjusted(
                image=models.Countries.objects.filter(code=self.code).first().flag,
                alt=None,
                size=size,
                rendition_key_set="country_flag",
                info=info,
            )

    def resolve_latitude(self, info, **_kwargs):
        return models.Countries.objects.filter(code=self.code).first().latitude

    def resolve_longitude(self, info, **_kwargs):
        return models.Countries.objects.filter(code=self.code).first().longitude


class Permission(graphene.ObjectType):
    code = PermissionEnum(description="Internal code for permission.", required=True)
    name = graphene.String(
        description="Describe action(s) allowed to do by permission.", required=True
    )

    class Meta:
        description = "Represents a permission object in a friendly form."


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class AccountError(Error):
    code = AccountErrorCode(description="The error code.", required=True)


class AnalyticsError(Error):
    code = AnalyticsErrorCode(description="The error code.", required=True)


class AppError(Error):
    code = AppErrorCode(description="The error code.", required=True)
    permissions = graphene.List(
        graphene.NonNull(PermissionEnum),
        description="List of permissions which causes the error.",
        required=False,
    )


class BlogError(Error):
    code = BlogErrorCode(description="The error code.", required=True)


class HelpdeskError(Error):
    code = HelpdeskErrorCode(description="The error code.", required=True)


class LanguageDisplay(graphene.ObjectType):
    code = LanguageCodeEnum(
        description="ISO 639 representation of the language name.", required=True
    )
    language = graphene.String(description="Full name of the language.", required=True)


class StaffError(AccountError):
    permissions = graphene.List(
        graphene.NonNull(PermissionEnum),
        description="List of permissions which causes the error.",
        required=False,
    )
    groups = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of permission group IDs which cause the error.",
        required=False,
    )
    users = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of user IDs which causes the error.",
        required=False,
    )


class MenuError(Error):
    code = MenuErrorCode(description="The error code.", required=True)


class MetadataError(Error):
    code = MetadataErrorCode(description="The error code.", required=True)


class NewsError(Error):
    code = NewsErrorCode(description="The error code.", required=True)


class OrderError(Error):
    code = OrderErrorCode(description="The error code.", required=True)
    warehouse = graphene.ID(
        description="Warehouse ID which causes the error.", required=False,
    )
    order_line = graphene.ID(
        description="Order line ID which causes the error.", required=False,
    )


class InvoiceError(Error):
    code = InvoiceErrorCode(description="The error code.", required=True)


class PermissionGroupError(Error):
    code = PermissionGroupErrorCode(description="The error code.", required=True)
    permissions = graphene.List(
        graphene.NonNull(PermissionEnum),
        description="List of permissions which causes the error.",
        required=False,
    )
    users = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of user IDs which causes the error.",
        required=False,
    )


class SiteError(Error):
    code = SiteErrorCode(description="The error code.", required=True)


class PageError(Error):
    code = PageErrorCode(description="The error code.", required=True)


class PaymentError(Error):
    code = PaymentErrorCode(description="The error code.", required=True)


class PluginError(Error):
    code = PluginErrorCode(description="The error code.", required=True)


class ProfileError(Error):
    code = ProfileErrorCode(description="The error code.", required=True)


class ProductError(Error):
    code = ProductErrorCode(description="The error code.", required=True)


class TranslationError(Error):
    code = TranslationErrorCode(description="The error code.", required=True)


class WebhookError(Error):
    code = WebhookErrorCode(description="The error code.", required=True)


class SeoInput(graphene.InputObjectType):
    title = graphene.String(description="SEO title.")
    description = graphene.String(description="SEO description.")


class BrochureFile(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the Brochure File.")
    alt = graphene.String(description="Alt text for an Brochure File.")
    size = graphene.String(description="size of Brochure File.")
    filename = graphene.String(description="file name of Brochure File.")
    name = graphene.String(description="file name of Brochure File.")

    class Meta:
        description = "Represents an Brochure."

    def resolve_url(root, info, **kwargs):
        return info.context.build_absolute_uri(root.url)



class PriceRangeInput(graphene.InputObjectType):
    gte = graphene.Float(description="Price greater than or equal to.", required=False)
    lte = graphene.Float(description="Price less than or equal to.", required=False)


class DateRangeInput(graphene.InputObjectType):
    gte = graphene.Date(description="Start date.", required=False)
    lte = graphene.Date(description="End date.", required=False)


class DateTimeRangeInput(graphene.InputObjectType):
    gte = graphene.DateTime(description="Start date.", required=False)
    lte = graphene.DateTime(description="End date.", required=False)


class IntRangeInput(graphene.InputObjectType):
    gte = graphene.Int(description="Value greater than or equal to.", required=False)
    lte = graphene.Int(description="Value less than or equal to.", required=False)


class TaxType(graphene.ObjectType):
    """Representation of tax types fetched from tax gateway."""

    description = graphene.String(description="Description of the tax type.")
    tax_code = graphene.String(
        description="External tax code used to identify given tax group."
    )


class Job(graphene.Interface):
    status = JobStatusEnum(description="Job status.", required=True)
    created_at = graphene.DateTime(
        description="Created date time of job in ISO 8601 format.", required=True
    )
    updated_at = graphene.DateTime(
        description="Date time of job last update in ISO 8601 format.", required=True
    )
    message = graphene.String(description="Job message.")

    @classmethod
    def resolve_type(cls, instance, _info):
        """Map a data object to a Graphene type."""
        MODEL_TO_TYPE_MAP = {
            # <DjangoModel>: <GrapheneType>
        }
        return MODEL_TO_TYPE_MAP.get(type(instance))
