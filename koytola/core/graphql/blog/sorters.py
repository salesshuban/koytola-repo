import graphene

from ..core.types import SortInputObjectType


class BlogSortField(graphene.Enum):
    TITLE = ["title", "slug"]
    SLUG = ["slug"]
    VISIBILITY = ["is_published", "title", "slug"]
    CREATION_DATE = ["creation_date", "title", "slug"]
    PUBLICATION_DATE = ["publication_date", "title", "slug"]

    @property
    def description(self):
        if self.name in BlogSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort blogs by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class BlogSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = BlogSortField
        type_name = "blogs"
