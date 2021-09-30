import graphene

from ..core.types import SortInputObjectType


class NewsSortField(graphene.Enum):
    TITLE = ["title", "pk"]
    SLUG = ["slug"]
    VISIBILITY = ["is_published", "title", "slug"]
    CREATION_DATE = ["creation_date", "title", "slug"]
    PUBLICATION_DATE = ["publication_date", "title", "slug"]
    UPDATE_DATE = ["update_date", "title", "slug"]

    @property
    def description(self):
        if self.name in NewsSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort news by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class NewsSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = NewsSortField
        type_name = "news"
