from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q
import graphene
from graphql import GraphQLError

from ...account import models as account_models
from ...core.error_codes import SiteErrorCode
from ...core.permissions import SitePermissions
from ...core.utils.url import validate_frontend_url
from ...site import ContactMessageStatus
from ...site import models as site_models
from ..account.i18n import I18nMixin
from ..account.types import AddressInput
from ..core.mutations import BaseMutation, ModelDeleteMutation, ModelMutation
from ..core.types.common import SiteError
from .enums import ContactMessageStatusEnum
from .types import (
    AuthorizationKey,
    AuthorizationKeyType,
    Site,
    SiteSubscriber,
    ContactMessage
)


class ContactMessageInput(graphene.InputObjectType):
    full_name = graphene.String(
        description="Full name of the sender.", required=True
    )
    email = graphene.String(
        description="Email of the message sender.", required=True
    )
    subject = graphene.String(
        description="Contact message subject.", required=True
    )
    content = graphene.String(
        description="Contact message content.", required=True
    )


class ContactMessageUpdateInput(ContactMessageInput):
    status = ContactMessageStatusEnum(description="Message Status.")
    note = graphene.String(description="Contact message notes.")


class SiteSettingsInput(graphene.InputObjectType):
    header_text = graphene.String(description="Header text.")
    description = graphene.String(description="SEO description.")
    include_taxes_in_prices = graphene.Boolean(description="Include taxes in prices.")
    display_gross_prices = graphene.Boolean(
        description="Display prices with tax in store."
    )
    default_mail_sender_name = graphene.String(
        description="Default email sender's name."
    )
    default_mail_sender_address = graphene.String(
        description="Default email sender's address."
    )
    account_set_password_url = graphene.String(
        description="URL of a view where accounts can set their password."
    )


class SiteDomainInput(graphene.InputObjectType):
    domain = graphene.String(description="Domain name for site.")
    name = graphene.String(description="Site site name.")


class SiteSubscriberInput(graphene.InputObjectType):
    email = graphene.String(
        description="Email of the subscriber.", required=True
    )


class SiteSubscriberUpdateInput(SiteSubscriberInput):
    is_active = graphene.Boolean(description="Subscription active status.")


class SiteSettingsUpdate(BaseMutation):
    site = graphene.Field(Site, description="Updated site.")

    class Arguments:
        input = SiteSettingsInput(
            description="Fields required to update site settings.", required=True
        )

    class Meta:
        description = "Updates site settings."
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def clean_input(cls, _info, _instance, data):
        if data.get("account_set_password_url"):
            try:
                validate_frontend_url(data["account_set_password_url"])
            except ValidationError as error:
                raise ValidationError(
                    {"account_set_password_url": error}, code=SiteErrorCode.INVALID
                )
        return data

    @classmethod
    def construct_instance(cls, instance, cleaned_data):
        for field_name, desired_value in cleaned_data.items():
            current_value = getattr(instance, field_name)
            if current_value != desired_value:
                setattr(instance, field_name, desired_value)
        return instance

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        instance = info.context.site.settings
        data = data.get("input")
        cleaned_input = cls.clean_input(info, instance, data)
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        instance.save()
        return SiteSettingsUpdate(site=Site())


class SiteAddressUpdate(BaseMutation, I18nMixin):
    site = graphene.Field(Site, description="Updated site.")

    class Arguments:
        input = AddressInput(description="Fields required to update site address.")

    class Meta:
        description = (
            "Update the site's address. If the `null` value is passed, the currently "
            "selected address will be deleted."
        )
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        site_settings = info.context.site.settings
        data = data.get("input")

        if data:
            if not site_settings.company_address:
                company_address = account_models.Address()
            else:
                company_address = site_settings.company_address
            company_address = cls.validate_address(data, company_address, info=info)
            company_address.save()
            site_settings.company_address = company_address
            site_settings.save(update_fields=["company_address"])
        else:
            if site_settings.company_address:
                site_settings.company_address.delete()
        return SiteAddressUpdate(site=Site())


class SiteDomainUpdate(BaseMutation):
    site = graphene.Field(Site, description="Updated site.")

    class Arguments:
        input = SiteDomainInput(description="Fields required to update site.")

    class Meta:
        description = "Updates site domain of the site."
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        site = info.context.site
        data = data.get("input")
        domain = data.get("domain")
        name = data.get("name")
        if domain is not None:
            site.domain = domain
        if name is not None:
            site.name = name
        cls.clean_instance(info, site)
        site.save()
        return SiteDomainUpdate(site=Site())


class AuthorizationKeyInput(graphene.InputObjectType):
    key = graphene.String(
        required=True, description="Client authorization key (client ID)."
    )
    password = graphene.String(required=True, description="Client secret.")


class AuthorizationKeyAdd(BaseMutation):
    authorization_key = graphene.Field(
        AuthorizationKey, description="Newly added authorization key."
    )
    site = graphene.Field(Site, description="Updated site.")

    class Meta:
        description = "Adds an authorization key."
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    class Arguments:
        key_type = AuthorizationKeyType(
            required=True, description="Type of an authorization key to add."
        )
        input = AuthorizationKeyInput(
            required=True, description="Fields required to create an authorization key."
        )

    @classmethod
    def perform_mutation(cls, _root, info, key_type, **data):
        if site_models.AuthorizationKey.objects.filter(name=key_type).exists():
            raise ValidationError(
                {
                    "key_type": ValidationError(
                        "Authorization key already exists.",
                        code=SiteErrorCode.ALREADY_EXISTS,
                    )
                }
            )

        site_settings = info.context.site.settings
        instance = site_models.AuthorizationKey(
            name=key_type, site_settings=site_settings, **data.get("input")
        )
        cls.clean_instance(info, instance)
        instance.save()
        return AuthorizationKeyAdd(authorization_key=instance, site=Site())


class AuthorizationKeyDelete(BaseMutation):
    authorization_key = graphene.Field(
        AuthorizationKey, description="Authorization key that was deleted."
    )
    site = graphene.Field(Site, description="Updated site.")

    class Arguments:
        key_type = AuthorizationKeyType(
            required=True, description="Type of a key to delete."
        )

    class Meta:
        description = "Deletes an authorization key."
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def perform_mutation(cls, _root, info, key_type):
        try:
            site_settings = info.context.site.settings
            instance = site_models.AuthorizationKey.objects.get(
                name=key_type, site_settings=site_settings
            )
        except site_models.AuthorizationKey.DoesNotExist:
            raise ValidationError(
                {
                    "key_type": ValidationError(
                        "Couldn't resolve authorization key",
                        code=SiteErrorCode.NOT_FOUND,
                    )
                }
            )

        instance.delete()
        return AuthorizationKeyDelete(authorization_key=instance, site=Site())


class StaffNotificationRecipientInput(graphene.InputObjectType):
    user = graphene.ID(
        required=False,
        description="The ID of the user subscribed to email notifications..",
    )
    email = graphene.String(
        required=False,
        description="Email address of a user subscribed to email notifications.",
    )
    active = graphene.Boolean(
        required=False, description="Determines if a notification active."
    )


class StaffNotificationRecipientCreate(ModelMutation):
    class Arguments:
        input = StaffNotificationRecipientInput(
            required=True,
            description="Fields required to create a staff notification recipient.",
        )

    class Meta:
        description = "Creates a new staff notification recipient."
        model = account_models.StaffNotificationRecipient
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        cls.validate_input(instance, cleaned_input)
        email = cleaned_input.pop("email", None)
        if email:
            staff_user = account_models.User.objects.filter(email=email).first()
            if staff_user:
                cleaned_input["user"] = staff_user
            else:
                cleaned_input["staff_email"] = email
        return cleaned_input

    @staticmethod
    def validate_input(instance, cleaned_input):
        email = cleaned_input.get("email")
        user = cleaned_input.get("user")
        if not email and not user:
            if instance.id and "user" in cleaned_input or "email" in cleaned_input:
                raise ValidationError(
                    {
                        "staff_notification": ValidationError(
                            "User and email cannot be set empty",
                            code=SiteErrorCode.INVALID,
                        )
                    }
                )
            if not instance.id:
                raise ValidationError(
                    {
                        "staff_notification": ValidationError(
                            "User or email is required", code=SiteErrorCode.REQUIRED
                        )
                    }
                )
        if user and not user.is_staff:
            raise ValidationError(
                {
                    "user": ValidationError(
                        "User has to be staff user", code=SiteErrorCode.INVALID
                    )
                }
            )


class StaffNotificationRecipientUpdate(StaffNotificationRecipientCreate):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a staff notification recipient to update."
        )
        input = StaffNotificationRecipientInput(
            required=True,
            description="Fields required to update a staff notification recipient.",
        )

    class Meta:
        description = "Updates a staff notification recipient."
        model = account_models.StaffNotificationRecipient
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"


class StaffNotificationRecipientDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a staff notification recipient to delete."
        )

    class Meta:
        description = "Delete staff notification recipient."
        model = account_models.StaffNotificationRecipient
        permissions = (SitePermissions.MANAGE_SETTINGS,)
        error_type_class = SiteError
        error_type_field = "site_errors"


class ContactMessageCreate(ModelMutation):
    class Arguments:
        input = ContactMessageInput(
            required=True, description="Fields required to create a contact message."
        )

    class Meta:
        description = "Creates a new contact message."
        model = site_models.ContactMessage
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return ContactMessage

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        if len(site_models.ContactMessage.objects.filter(
            Q(email=data["email"]) &
            Q(status=ContactMessageStatus.SPAM) &
            Q(date_submitted__gte=datetime.now() - timedelta(days=30)))
        ) >= 3 or len(site_models.ContactMessage.objects.filter(
            Q(email=data["email"]) &
            Q(status=ContactMessageStatus.NEW) &
            Q(date_submitted__gte=datetime.now() - timedelta(days=30)))
        ) >= 5:
            raise GraphQLError('You have sent too many messages. Your submission is disabled.')
        return cleaned_input


class ContactMessageUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a contact message to update.")
        input = ContactMessageUpdateInput(
            required=True, description="Fields required to create a contact message."
        )

    class Meta:
        description = "Creates a new contact message."
        model = site_models.ContactMessage
        permissions = (SitePermissions.MANAGE_CONTACT_MESSAGES,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return ContactMessage


class ContactMessageDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True,
            description="ID of a contact message to delete."
        )

    class Meta:
        description = "Deletes a contact message."
        model = site_models.ContactMessage
        permissions = (SitePermissions.MANAGE_CONTACT_MESSAGES,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return ContactMessage


class SiteSubscriberCreate(ModelMutation):
    class Arguments:
        input = SiteSubscriberInput(
            required=True, description="Fields required to create a subscriber."
        )

    class Meta:
        description = "Creates a new subscriber."
        model = site_models.SiteSubscriber
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        if site_models.SiteSubscriber.objects.filter(Q(email__iexact=data["email"])):
            raise GraphQLError('You are already subscribed to our newsletter.')
        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return SiteSubscriber


class SiteSubscriberUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a subscriber to update.")
        input = SiteSubscriberUpdateInput(
            required=True, description="Fields required to update a subscriber."
        )

    class Meta:
        description = "Creates a new subscriber."
        model = site_models.SiteSubscriber
        permissions = (SitePermissions.MANAGE_SITE_SUBSCRIBERS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return SiteSubscriber


class SiteSubscriberDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a subscriber to delete.")

    class Meta:
        description = "Deletes a subscriber."
        model = site_models.SiteSubscriber
        permissions = (SitePermissions.MANAGE_SITE_SUBSCRIBERS,)
        error_type_class = SiteError
        error_type_field = "site_errors"

    @classmethod
    def get_type_for_model(cls):
        return SiteSubscriber
