import graphene

from ..core.types import SortInputObjectType


class ContactMessageSortField(graphene.Enum):
    DATE_SUBMITTED = ["date_submitted", "pk"]
    DATE_UPDATED = ["date_updated", "pk"]
    EMAIL = ["email", "pk"]
    NAME = ["full_name", "pk"]
    SUBJECT = ["subject", "pk"]

    @property
    def description(self):
        if self.name in ContactMessageSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort contact messages by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ContactMessageSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = ContactMessageSortField
        type_name = "contact_messages"


class SiteSubscriberSortField(graphene.Enum):
    EMAIL = ["email", "pk"]
    CREATION_DATE = ["creation_date", "pk"]

    @property
    def description(self):
        if self.name in SiteSubscriberSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort subscribers by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class SiteSubscriberSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = SiteSubscriberSortField
        type_name = "subscribers"
