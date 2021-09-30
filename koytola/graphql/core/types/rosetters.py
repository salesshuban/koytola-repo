from ..connection import CountableDjangoObjectType
import graphene
from ...core.types import Image
from graphene import relay
from ....profile import models
from ...core.scalars import Array


class Roetter(CountableDjangoObjectType):
    image = graphene.Field(
        lambda: Image,
        size=graphene.Int(description="Success Story image sizes.")
    )
    category = Array()

    class Meta:
        description = ("Company Industry list.", )
        only_fields = ["id", "type", "name", "is_active", "created_at", "updated_at"]
        interfaces = [relay.Node]
        model = models.Roetter

    @staticmethod
    def resolve_category(root: models.Roetter, info, **_kwargs):
        if root.category:
            return eval(root.category)
        else:
            return []

    @staticmethod
    def resolve_image(root: models.Roetter, info, size=None, **_kwargs):
        if root.image:
            return Image.get_adjusted(
                image=root.image,
                alt=root.name,
                size=size,
                rendition_key_set="images",
                info=info,
            )
