import graphene

from ..core.types import SortInputObjectType


class CompanySortField(graphene.Enum):
    SLUG = ["slug", "pk"]
    NAME = ["name", "pk"]
    DATE_CREATED = ["creation_date", "pk"]

    @property
    def description(self):
        if self.name in CompanySortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort companies by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ContactsSortField(graphene.Enum):
    NAME = ["name", "pk"]
    EMAIL = ["email", "pk"]
    COUNTRY = ["country", "pk"]
    CONTACT = ["contact", "pk"]

    @property
    def description(self):
        if self.name in ContactsSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort contact by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class SocialResponsibilitySortField(graphene.Enum):
    NAME = ["name", "pk"]
    BROCHUREFILENAME = ["brochure_file_name", "pk"]
    DATE_CREATED = ["created_at", "pk"]
    DESCRIPTION = ["description", "pk"]


class CompanySortingInput(SortInputObjectType):
    class Meta:
        sort_enum = CompanySortField
        type_name = "companies"


class ContactsSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = ContactsSortField
        type_name = "contacts"


class SocialResponsibilitySortingInput(SortInputObjectType):
    class Meta:
        sort_enum = SocialResponsibilitySortField
        type_name = "social_responsibility"


class SuccessStorySortField(graphene.Enum):
    TITLE = ["title", "pk"]
    NAME = ["name", "pk"]
    COMPANYNAME = ["company_name", "pk"]
    SLUG = ["slug", "pk"]
    LOCATION = ["location", "pk"]


class TradeShowsSortField(graphene.Enum):
    YEAR = ["year", "pk"]
    NAME = ["name", "pk"]
    CITY = ["city", "pk"]
    SLUG = ["slug", "pk"]
    COMPANYNAME = ["company_name", "pk"]


class IndexSortField(graphene.Enum):
    INDEX = ["index", "pk"]


class SuccessStorySortingInput(SortInputObjectType):
    class Meta:
        sort_enum = SuccessStorySortField
        type_name = "success_story"


class TradeShowsInput(SortInputObjectType):
    class Meta:
        sort_enum = TradeShowsSortField
        type_name = "trade_shows"


class IndexSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = IndexSortField
        type_name = "index"
