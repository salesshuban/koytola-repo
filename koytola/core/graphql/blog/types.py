import graphene
from graphene import relay
from graphene_federation import key
from ...blog import models
from ..core.connection import CountableDjangoObjectType
from ..translations.fields import TranslationField
from ..translations.types import BlogTranslation
from ..core.types import Image
from ...graphql.utils import get_user_or_app_from_context
from ..core.scalars import Array



@key("id")
@key("slug")
class BlogCategory(CountableDjangoObjectType):
    blogs = graphene.List(
        lambda: Blog,
        description="List of products under the category."
    )
    children = graphene.List(
        lambda: BlogCategory, description="List of children of the category."
    )
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Offer image sizes.")
    )
    tags = Array(description="Blog Category`s tags.")

    class Meta:
        description = (
            "Blog Category"
        )
        only_fields = [
            "name",
            "slug",
            "description",
            "id",
            "description_plaintext",
            "parent",
            "background_image_alt"
        ]
        interfaces = [relay.Node]
        model = models.BlogCategory

    @staticmethod
    def resolve_tags(root: models.BlogCategory, info, **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_background_image(root: models.BlogCategory, info, size=None, **_kwargs):
        if root.background_image:
            return Image.get_adjusted(
                image=root.background_image,
                alt=root.background_image_alt,
                size=size,
                rendition_key_set="background_images",
                info=info,
            )

    @staticmethod
    def resolve_children(root: models.BlogCategory, info, **_kwargs):
        return root.children.all()

    @staticmethod
    def resolve_blogs(root: models.BlogCategory, info, **_kwargs):
        qs = models.Blog.objects.filter(category_id=root.id)
        return qs


@key("id")
@key("slug")
class Blog(CountableDjangoObjectType):
    translation = TranslationField(BlogTranslation, type_name="blog")
    tags = Array(description="Blog`s tags")
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Offer image sizes.")
    )
    category = graphene.List(BlogCategory, description="blog categories")

    class Meta:
        description = (
            "A static blog that can be manually added by a shop operator through the "
            "dashboard."
        )
        only_fields = [
            "id",
            "user",
            "short_description",
            "description",
            "is_published",
            "publication_date",
            "updated_at",
            "seo_description",
            "seo_title",
            "slug",
            "title",
            "created_at"
        ]
        interfaces = [relay.Node]
        model = models.Blog

    @staticmethod
    def resolve_tags(root: models.Blog, info, **_kwargs):
        if root.tags:
            return eval(root.tags)

    @staticmethod
    def resolve_category(root: models.Blog, info, **_kwargs):
        return root.category.all()

    @staticmethod
    def resolve_image(root: models.Blog, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.title,
                size=size,
                rendition_key_set="images",
                info=info,
            )
