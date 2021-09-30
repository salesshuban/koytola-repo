import graphene

from ..core.types import SortInputObjectType


class TrackingSortField(graphene.Enum):
    DATE = ["date", "pk"]
    TYPE = ["type", "pk"]
    USER = ["user", "pk"]
    CATEGORY = ["category", "pk"]
    COMPANY = ["company", "pk"]
    PRODUCT = ["product", "pk"]

    IP = ["ip", "pk"]
    COUNTRY = ["country", "pk"]
    REGION = ["region", "pk"]
    CITY = ["city", "pk"]
    REFERRER = ["referrer", "pk"]
    DEVICE_TYPE = ["device_type", "pk"]
    BROWSER = ["browser", "pk"]

    @property
    def description(self):
        if self.name in TrackingSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort trackings by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class TrackingSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = TrackingSortField
        type_name = "trackings"


class UserTrackingSortField(graphene.Enum):
    DATE = ["date", "pk"]
    TYPE = ["type", "pk"]
    COMPANY = ["company", "pk"]
    PRODUCT = ["product", "pk"]

    @property
    def description(self):
        if self.name in TrackingSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort trackings by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class UserTrackingSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = UserTrackingSortField
        type_name = "user_trackings"
