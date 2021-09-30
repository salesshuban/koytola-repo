import graphene

from ..core.types import SortInputObjectType


class UserSortField(graphene.Enum):
    FIRST_NAME = ["first_name", "last_name", "pk"]
    LAST_NAME = ["last_name", "first_name", "pk"]
    EMAIL = ["email"]
    DATE_JOINED = ["date_joined", "email"]
    LAST_LOGIN = ["last_login", "email"]

    @property
    def description(self):
        if self.name in UserSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort users by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class UserSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = UserSortField
        type_name = "users"


class PermissionGroupSortField(graphene.Enum):
    NAME = ["name"]

    @property
    def description(self):
        # pylint: disable=no-member
        if self in [PermissionGroupSortField.NAME]:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort permission group accounts by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class PermissionGroupSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = PermissionGroupSortField
        type_name = "permission group"


class EventSortField(graphene.Enum):
    NAME = ["user__email", "pk"]
    DATE = ["date", "pk"]
    TYPE = ["type", "date"]
    MEMBERSHIP = ["membership", "date"]
    ORDER = ["order", "date"]
    PROFILE = ["profile", "date"]
    SUBSCRIPTION = ["subscription", "date"]

    @property
    def description(self):
        if self.name in EventSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort events by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class EventSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = EventSortField
        type_name = "events"
