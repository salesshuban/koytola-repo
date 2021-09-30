import graphene
from django.core.exceptions import ValidationError
from ....profile import models
from ....profile.error_codes import ProfileErrorCode
from ...core.types import Upload
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ProfileError
from ...core.utils import (
    validate_slug_and_generate_if_needed
)
from ...profile.types import TradeShow, Company
from ....core.utils import generate_unique_slug
from ....core.permissions import ProfilePermissions


class TradeShowInput(graphene.InputObjectType):
    name = graphene.String(description="Trade Show name")
    year = graphene.Int(description="Trade Show year")
    city = graphene.String(description="Trade Show city")


class TradeShowCreate(ModelMutation):
    tradeShow = graphene.Field(
        TradeShow, description="create trade_show."
    )

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add contact."
        )
        input = TradeShowInput(
            required=True, description="Fields required to create a contact."
        )

    class Meta:
        description = "Creates a new contact."
        model = models.TradeShow
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info, company_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        instance = cls.get_instance(info, **data)
        instance.company = company
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return TradeShowCreate(tradeShow=instance)

    @classmethod
    def get_type_for_model(cls):
        return TradeShow
