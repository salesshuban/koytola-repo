import graphene

from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types.common import ProfileError
from ...profile.types import Company, Contact
from ..enums import MessageStatusEnum, MessageTypeEnum
from ..utils import (
    company_permission,
    contact_filter
)


class ContactInput(graphene.InputObjectType):
    name = graphene.String(description="Name of the sender.")
    email = graphene.String(description="The email of the sender.")
    country = graphene.String(description="The country of the contact.")
    subject = graphene.String(description="The subject of the contact.", required=False)
    contact = graphene.String(description="The content of the contact.")
    type = MessageTypeEnum(description="Contact message type.", required=False)
    status = MessageStatusEnum(description="Contact message status.", required=False)


class ContactUpdateInput(graphene.InputObjectType):
    status = MessageStatusEnum(description="Contact message status.", required=False)
    type = MessageTypeEnum(description="Contact message type.", required=False)


class ContactCreate(ModelMutation):
    contact = graphene.Field(
        Contact, description="An updated contact."
    )

    class Arguments:

        input = ContactInput(
            required=True, description="Fields required to create a contact."
        )

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    class Meta:
        description = "Creates a new contact."
        model = models.Contact
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def perform_mutation(cls, root, info,  **data):
        contact_filter(data)
        instance = cls.get_instance(info, **data)
        instance.user = info.context.user
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return ContactCreate(contact=instance)

    @classmethod
    def get_type_for_model(cls):
        return Contact


class ContactUpdate(ModelMutation):
    contact = graphene.Field(
        Contact, description="An updated contact."
    )

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a contact to delete."
        )
        input = ContactInput(
            required=True, description="Fields to update in your contact message."
        )

    class Meta:
        description = "Updates a contact."
        model = models.Contact
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        contact = cls.get_node_or_error(
            info, id, only_type=Contact, field="id"
        )
        # company_permission(info, contact.company)
        cleaned_input = cls.clean_input(info, contact, data.get("input"))
        contact = cls.construct_instance(contact, cleaned_input)
        cls.clean_instance(info, contact)
        cls.save(info, contact, cleaned_input)
        return ContactUpdate(contact=contact)

    @classmethod
    def get_type_for_model(cls):
        return Contact


class ContactDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a contact to delete."
        )

    class Meta:
        description = "Deletes a contact."
        model = models.Contact
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        contact = cls.get_node_or_error(
            info, id, only_type=Contact, field="id"
        )
        contact.delete()
        return ContactDelete(contact=contact)


class ContactBulkDelete(ModelDeleteMutation):
    contact = graphene.Field(
        Contact, description="An updated contact."
    )

    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of company contacts to delete."
        )

    class Meta:
        description = "Deletes  contacts."
        model = models.Contact
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info,  **data):

        for id in data['ids']:
            contact = cls.get_node_or_error(info, id, only_type=Contact, field="id")
            contact.delete()
        return ContactDelete()
