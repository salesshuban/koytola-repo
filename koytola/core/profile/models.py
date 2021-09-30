from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
import datetime
from mptt.models import MPTTModel
from ..account.models import PossiblePhoneNumberField
from ..core.db.fields import SanitizedJSONField
from ..core.models import PublishableModel, SortableModel
from ..core.permissions import ProfilePermissions
from ..core.utils.editorjs import clean_editor_js
from ..seo.models import SeoModel
from versatileimagefield.fields import VersatileImageField
from ..core.utils import upload_path_handler
from ..account.models import Address, User
from . import (
    CompanySize,
    CompanyType,
    EmployeeNumber,
    MessageType,
    MessageStatus,
)
from phonenumber_field.modelfields import PhoneNumberField


class CompanyQuerySet(models.QuerySet):
    def published(self):
        today = datetime.date.today()
        return self.filter(
            Q(publication_date__lte=today) | Q(publication_date__isnull=True),
            is_published=True,
        )

    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(ProfilePermissions.MANAGE_PROFILES)

    def visible_to_user(self, user):
        if self.user_has_access_to_all(user):
            return self.all()
        return self.filter(user=user)


class Industry(MPTTModel):
    name = models.CharField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Roetter(models.Model):
    type = models.CharField(max_length=250, choices=(('Company', 'Company'), ('Product', 'Product')))
    name = models.CharField(max_length=250)
    category = models.TextField(max_length=65500, null=True, blank=True)
    image = VersatileImageField(upload_to="rosetter/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Company(SeoModel, PublishableModel):
    user = models.OneToOneField(
        User,
        related_name="companies",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)
    name = models.CharField(max_length=250, unique=True, null=True, blank=True)
    website = models.URLField(blank=True, default="")
    # email = models.EmailField(blank=True, default="", unique=False)
    phone = PossiblePhoneNumberField(max_length=128, blank=True, null=True)
    logo = VersatileImageField(
        upload_to=upload_path_handler, blank=True, null=True
    )
    logo_alt = models.CharField(max_length=128, blank=True)
    address = models.ForeignKey(
        Address,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    founded_year = models.IntegerField(
        validators=[
            MaxValueValidator(2100),
            MinValueValidator(1800)
        ],
        default=datetime.date.today().year,
        blank=True,
        null=True
    )
    no_of_employees = models.CharField(
        max_length=32,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in EmployeeNumber.CHOICES
        ],
        default=EmployeeNumber.CHOICES[0][0],
        blank=True,
        null=True
    )
    content = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_editor_js
    )
    content_plaintext = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    brands = models.TextField(blank=True, default="[]")
    rosetter = models.ManyToManyField(Roetter, related_name="company_rosetter+", blank=True)
    membership = models.TextField(blank=True, default="[]")
    is_brand = models.BooleanField(default=False)
    industry = models.ForeignKey(
        Industry,
        related_name="company_industry",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    export_countries = CountryField(blank=True, multiple=True)
    size = models.CharField(
        max_length=32,
        choices=CompanySize.CHOICES,
        default=CompanySize.NONE,
    )
    type = models.CharField(
        max_length=32,
        choices=CompanyType.CHOICES,
        default=CompanyType.MANUFACTURER,
    )
    organic_products = models.BooleanField(default=False)
    private_label = models.BooleanField(default=False)
    female_leadership = models.BooleanField(default=False)
    branded_value = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    objects = CompanyQuerySet.as_manager()

    class Meta:
        ordering = ["slug"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        permissions = [
            (
                ProfilePermissions.MANAGE_PROFILES.codename,
                "Manage profiles."
            )
        ]

    def __str__(self):
        return self.name


class TradeShow(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_trade_show")
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    city = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Representative(models.Model):
    company = models.ForeignKey(
        Company,
        related_name="representative",
        on_delete=models.SET_NULL,
        null=True
    )
    photo = VersatileImageField(
        upload_to=upload_path_handler, blank=True, null=True
    )
    photo_alt = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=250)
    position = models.CharField(
        max_length=250,
        blank=False,
        default="Customer Representative"
    )
    linkedin_url = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "Company Representative"
        verbose_name_plural = "Company Representatives"


class CertificateType(models.Model):
    type = models.CharField(max_length=250, choices=[("Company", "Company"), ("Product", "Product")])
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    image = VersatileImageField(
        upload_to=upload_path_handler, blank=True, null=True
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Certificate(SortableModel):
    company = models.ForeignKey(
        Company,
        related_name="certificates",
        on_delete=models.SET_NULL,
        null=True
    )
    certificate = models.FileField(upload_to=upload_path_handler, blank=True)
    # name = models.CharField(max_length=128, blank=True)
    type = models.ForeignKey(CertificateType,
                             related_name="certificate_type",
                             on_delete=models.SET_NULL,
                             null=True
                             )

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Company Certificate"
        verbose_name_plural = "Company Certificates"
    #
    # def __str__(self):
    #     return self.name

    def get_ordering_queryset(self):
        return self.company.certificates.all()


class Brochure(SortableModel):
    company = models.ForeignKey(
        Company,
        related_name="brochures",
        on_delete=models.SET_NULL,
        null=True
    )
    brochure = models.FileField(upload_to=upload_path_handler, blank=True)
    name = models.CharField(max_length=128, blank=True)
    index = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Company Brochure"
        verbose_name_plural = "Company Brochures"

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.company.brochures.all()


class Images(SortableModel):
    company = models.ForeignKey(
        Company,
        related_name="images",
        on_delete=models.SET_NULL,
        null=True
    )
    image = VersatileImageField(
        upload_to=upload_path_handler, blank=True, null=True
    )
    name = models.CharField(max_length=128, blank=True)
    index = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Company Images"
        verbose_name_plural = "Company Images"

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.company.images.all()


class Video(SortableModel):
    company = models.ForeignKey(
        Company,
        related_name="videos",
        on_delete=models.SET_NULL,
        null=True
    )
    video = models.FileField(upload_to=upload_path_handler, blank=True)
    youtube_url = models.URLField(blank=True)
    name = models.CharField(max_length=128, blank=True)
    index = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Company Video"
        verbose_name_plural = "Company Videos"

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.company.videos.all()


class SocialResponsibility(SortableModel):
    company = models.ForeignKey(
        Company,
        related_name="social_responsibilities",
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=128, blank=True)
    video = models.FileField(upload_to=upload_path_handler, blank=True)
    youtube_url = models.URLField(blank=True)
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    brochure = models.FileField(upload_to=upload_path_handler, blank=True)
    brochure_file_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=65500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = "Company Social Responsibility"
        verbose_name_plural = "Company Social Responsibilities"

    def __str__(self):
        return self.name

    def get_ordering_queryset(self):
        return self.company.social_responsibilities.all()


class Contact(models.Model):
    company = models.ForeignKey(
        Company,
        related_name="contact_messages",
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=32, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    country = models.CharField(max_length=64, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    ask_for_reference = models.BooleanField(default=False)
    subject = models.CharField(max_length=128, null=True, blank=True)
    contact = PhoneNumberField(max_length=128, blank=True, null=True)
    type = models.CharField(
        max_length=32,
        choices=MessageType.CHOICES,
        default=MessageType.INFO,
        blank=True
    )
    status = models.CharField(
        max_length=32,
        choices=MessageStatus.CHOICES,
        default=MessageStatus.NEW,
        blank=True
    )

    class Meta:
        ordering = ["-submission_date"]
        verbose_name = "Company Contact Data"
        verbose_name_plural = "Company Contact Data"

    def __str__(self):
        return self.name + ' - ' + self.email + ' from ' + self.company.name + ' at ' + \
            str(self.submission_date.strftime("%b-%d-%Y - %H:%M:%S"))


class SuccessStory(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=65550, blank=True, null=True)
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    tags = models.TextField(max_length=6550, blank=True, default="[]")
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
