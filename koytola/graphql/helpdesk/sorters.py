import graphene

from ..core.types import SortInputObjectType


class HelpdeskSortField(graphene.Enum):
    CREATION_DATE = ["creation_date", "type", "subject"]
    STATUS = ["status", "type", "subject"]
    SUBJECT = ["subject", "slug"]
    TYPE = ["type"]
    UPDATE_DATE = ["update_date", "type", "subject"]
    USER = ["user"]

    @property
    def description(self):
        if self.name in HelpdeskSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort tickets by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class HelpdeskSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = HelpdeskSortField
        type_name = "tickets"
