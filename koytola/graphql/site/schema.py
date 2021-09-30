import graphene

from ..core.fields import FilterInputConnectionField
from ..translations.mutations import SiteSettingsTranslate
from .bulk_mutations import (
    ContactMessageBulkDelete,
    ContactMessageBulkUpdate,
    SiteSubscriberBulkDelete,
    SiteSubscriberBulkUpdate,
)
from .filters import (
    ContactMessageFilterInput,
    SiteSubscriberFilterInput,
)
from .mutations import (
    AuthorizationKeyAdd,
    AuthorizationKeyDelete,
    SiteAddressUpdate,
    SiteDomainUpdate,
    SiteSettingsUpdate,
    StaffNotificationRecipientCreate,
    StaffNotificationRecipientDelete,
    StaffNotificationRecipientUpdate,
    ContactMessageCreate,
    ContactMessageUpdate,
    ContactMessageDelete,
    SiteSubscriberCreate,
    SiteSubscriberUpdate,
    SiteSubscriberDelete
)
from .resolvers import (
    resolve_contact_message,
    resolve_contact_messages,
    resolve_site_subscriber,
    resolve_site_subscribers
)
from .sorters import (
    ContactMessageSortingInput,
    SiteSubscriberSortingInput,
)
from .types import (
    Site,
    ContactMessage,
    SiteSubscriber,
)


class SiteQueries(graphene.ObjectType):
    site = graphene.Field(
        Site, description="Return information about the site.", required=True
    )
    contact_message = graphene.Field(
        ContactMessage,
        id=graphene.Argument(graphene.ID, description="ID of the contact message."),
        description="Look up a contact message by ID.",
    )
    contact_messages = FilterInputConnectionField(
        ContactMessage,
        sort_by=ContactMessageSortingInput(description="Sort contact messages."),
        filter=ContactMessageFilterInput(description="Filtering options for contact messages."),
        description="List of the site's contact messages.",
    )
    site_subscriber = graphene.Field(
        SiteSubscriber,
        id=graphene.Argument(graphene.ID, description="ID of the subscriber."),
        description="Look up a subscriber by ID.",
    )
    site_subscribers = FilterInputConnectionField(
        SiteSubscriber,
        sort_by=SiteSubscriberSortingInput(description="Sort subscribers."),
        filter=SiteSubscriberFilterInput(description="Filtering options for subscribers."),
        description="List of the site's subscribers.",
    )

    def resolve_site(self, _info):
        return Site()

    def resolve_contact_message(self, info, id=None):
        return resolve_contact_message(info, id)

    def resolve_contact_messages(self, info, **kwargs):
        return resolve_contact_messages(info, **kwargs)

    def resolve_site_subscriber(self, info, id=None):
        return resolve_site_subscriber(info, id)

    def resolve_site_subscribers(self, info, **kwargs):
        return resolve_site_subscribers(info, **kwargs)


class SiteMutations(graphene.ObjectType):
    authorization_key_add = AuthorizationKeyAdd.Field()
    authorization_key_delete = AuthorizationKeyDelete.Field()

    staff_notification_recipient_create = StaffNotificationRecipientCreate.Field()
    staff_notification_recipient_update = StaffNotificationRecipientUpdate.Field()
    staff_notification_recipient_delete = StaffNotificationRecipientDelete.Field()

    site_domain_update = SiteDomainUpdate.Field()
    site_settings_update = SiteSettingsUpdate.Field()
    site_settings_translate = SiteSettingsTranslate.Field()
    site_address_update = SiteAddressUpdate.Field()

    contact_message_create = ContactMessageCreate.Field()
    contact_message_update = ContactMessageUpdate.Field()
    contact_message_delete = ContactMessageDelete.Field()
    contact_message_bulk_update = ContactMessageBulkUpdate.Field()
    contact_message_bulk_delete = ContactMessageBulkDelete.Field()

    site_subscriber_create = SiteSubscriberCreate.Field()
    site_subscriber_update = SiteSubscriberUpdate.Field()
    site_subscriber_delete = SiteSubscriberDelete.Field()
    site_subscriber_bulk_update = SiteSubscriberBulkUpdate.Field()
    site_subscriber_bulk_delete = SiteSubscriberBulkDelete.Field()
