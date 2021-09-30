from email.headerregistry import Address
from email.utils import parseaddr
from typing import Optional

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from ..core.permissions import SitePermissions
from ..core.utils.translations import TranslationProxy
from . import AuthenticationBackends, ContactMessageStatus
from .error_codes import SiteErrorCode
from .patch_sites import patch_contrib_sites


patch_contrib_sites()


def email_sender_name_validators():
    return [
        RegexValidator(
            r"[\n\r]",
            inverse_match=True,
            message="New lines are not allowed.",
            code=SiteErrorCode.FORBIDDEN_CHARACTER.value,
        ),
        MaxLengthValidator(settings.DEFAULT_MAX_EMAIL_DISPLAY_NAME_LENGTH),
    ]


class SiteSettings(models.Model):
    site = models.OneToOneField(Site, related_name="settings", on_delete=models.CASCADE)
    header_text = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500, blank=True)
    top_menu = models.ForeignKey(
        "menu.Menu", on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )
    bottom_menu = models.ForeignKey(
        "menu.Menu", on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )
    company_address = models.ForeignKey(
        "account.Address", blank=True, null=True, on_delete=models.SET_NULL
    )
    default_mail_sender_name = models.CharField(
        max_length=settings.DEFAULT_MAX_EMAIL_DISPLAY_NAME_LENGTH,
        blank=True,
        default="",
        validators=email_sender_name_validators(),
    )
    default_mail_sender_address = models.EmailField(blank=True, null=True)
    account_set_password_url = models.CharField(max_length=255, blank=True, null=True)
    translated = TranslationProxy()

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
        permissions = (
            (SitePermissions.MANAGE_SETTINGS.codename, "Manage settings."),
            (SitePermissions.MANAGE_TRANSLATIONS.codename, "Manage translations."),
        )

    def __str__(self):
        return self.site.name

    @property
    def default_from_email(self) -> str:
        sender_name: str = self.default_mail_sender_name
        sender_address: Optional[str] = self.default_mail_sender_address

        if not sender_address:
            sender_address = settings.DEFAULT_FROM_EMAIL

            if not sender_address:
                raise ImproperlyConfigured("No sender email address has been set-up")

            sender_name, sender_address = parseaddr(sender_address)

        # Note: we only want to format the address in accordance to RFC 5322
        # but our job is not to sanitize the values. The sanitized value, encoding, etc.
        # will depend on the email backend being used.
        #
        # Refer to email.header.Header and django.core.mail.message.sanitize_address.
        value = str(Address(sender_name, addr_spec=sender_address))
        return value

    def available_backends(self):
        return self.authorizationkey_set.values_list("name", flat=True)


class SiteSettingsTranslation(models.Model):
    language_code = models.CharField(max_length=10)
    site_settings = models.ForeignKey(
        SiteSettings, related_name="translations", on_delete=models.CASCADE
    )
    header_text = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Site Settings Translation'
        verbose_name_plural = 'Site Settings Translations'
        unique_together = (("language_code", "site_settings"),)

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, site_settings_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.site_settings_id,
        )

    def __str__(self):
        return self.site_settings.site.name


class AuthorizationKey(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, choices=AuthenticationBackends.BACKENDS)
    key = models.TextField()
    password = models.TextField()

    class Meta:
        verbose_name = 'Authorization Key'
        verbose_name_plural = 'Authorization Keys'
        unique_together = (("site_settings", "name"),)

    def __str__(self):
        return self.name

    def key_and_secret(self):
        return self.key, self.password


class SiteSubscriber(models.Model):
    email = models.EmailField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Site Subscriber"
        verbose_name_plural = "Site Subscribers"
        permissions = [
            (
                SitePermissions.MANAGE_SITE_SUBSCRIBERS.codename,
                "Manage site subscribers."
            )
        ]


class Image(models.Model):
    image = models.FileField(
        verbose_name="Image",
        upload_to='images/',
        max_length=255,
        null=True,
        blank=True,
        default=''
    )
    alt_text = models.CharField(max_length=256, default='', null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=256, default='', null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ['-creation_date']
        permissions = [
            (
                SitePermissions.MANAGE_SITE_IMAGES.codename,
                "Manage site images."
            )
        ]


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    date_submitted = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=128, default="")
    content = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=255,
        choices=ContactMessageStatus.CHOICES,
        default=ContactMessageStatus.NEW
    )
    note = models.TextField(null=True, blank=True, default="")
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        permissions = [
            (
                SitePermissions.MANAGE_CONTACT_MESSAGES.codename,
                "Manage contact messages."
            )
        ]

    def __str__(self):
        return self.subject + ' at ' + str(self.date_submitted.strftime("%b-%d-%Y - %H:%M:%S"))
