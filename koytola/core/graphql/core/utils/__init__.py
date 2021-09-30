import binascii
import datetime
from typing import TYPE_CHECKING, Type, Union

import graphene
from django.core.exceptions import ValidationError
from graphene import ObjectType

from ....core.utils import generate_unique_slug

if TYPE_CHECKING:
    # flake8: noqa
    from django.db.models import Model


def clean_seo_fields(data):
    """Extract and assign seo fields to given dictionary."""
    seo_fields = data.pop("seo", None)
    if seo_fields:
        data["seo_title"] = seo_fields.get("title")
        data["seo_description"] = seo_fields.get("description")


def update_publication_date(data, instance=None):
    data_publication_date = data.get("publication_date", False)
    data_is_published = data.get("is_published", False)
    if data_is_published and not data_publication_date:
        if instance and hasattr(instance, "is_published"):
            if not instance.is_published:
                data["publication_date"] = datetime.datetime.now()
                data["is_published"] = True
        else:
            data["publication_date"] = datetime.datetime.now()
            data["is_published"] = True
    elif not data_is_published:
        if instance and hasattr(instance, "publication_date") and not data_publication_date:
            data["publication_date"] = None
        else:
            if not data_publication_date:
                data["publication_date"] = None
        data["is_published"] = False


def snake_to_camel_case(name):
    """Convert snake_case variable name to camelCase."""
    if isinstance(name, str):
        split_name = name.split("_")
        return split_name[0] + "".join(map(str.capitalize, split_name[1:]))
    return name


def str_to_enum(name):
    """Create an enum value from a string."""
    return name.replace(" ", "_").replace("-", "_").upper()


def validate_image_file(file, field_name):
    """Validate if the file is an image."""
    if not file:
        raise ValidationError(
            {field_name: ValidationError("File is required", code="required")}
        )
    if not file.content_type.startswith("image/"):
        raise ValidationError(
            {field_name: ValidationError("Invalid file type", code="invalid")}
        )


def from_global_id_strict_type(
    global_id: str, only_type: Union[ObjectType, str], field: str = "id"
) -> str:
    """Resolve a node global id with a strict given type required."""
    try:
        _type, _id = graphene.Node.from_global_id(global_id)
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValidationError(
            {
                field: ValidationError(
                    "Couldn't resolve to a node: %s" % global_id, code="not_found"
                )
            }
        ) from exc

    if str(_type) != str(only_type):
        raise ValidationError(
            {field: ValidationError(f"Must receive a {only_type} id", code="invalid")}
        )
    return _id


def validate_slug_and_generate_if_needed(
    instance: Type["Model"],
    slugable_field: str,
    cleaned_input: dict,
    slug_field_name: str = "slug",
) -> dict:
    """Validate slug from input and generate in create mutation if is not given."""

    # update mutation - just check if slug value is not empty
    # _state.adding is True only when it's new not saved instance.
    if not instance._state.adding:  # type: ignore
        validate_slug_value(cleaned_input)
        return cleaned_input

    # create mutation - generate slug if slug value is empty
    slug = cleaned_input.get(slug_field_name)
    if not slug and slugable_field in cleaned_input:
        slug = generate_unique_slug(instance, cleaned_input[slugable_field])
        cleaned_input[slug_field_name] = slug
    return cleaned_input


def validate_slug_value(cleaned_input, slug_field_name: str = "slug"):
    if slug_field_name in cleaned_input:
        slug = cleaned_input[slug_field_name]
        if not slug:
            raise ValidationError(
                f"{slug_field_name.capitalize()} value cannot be blank."
            )


def get_duplicates_ids(first_list, second_list):
    """Return items that appear on both provided lists."""
    if first_list and second_list:
        return set(first_list) & set(second_list)
    return []


def get_duplicated_values(values):
    """Return set of duplicated values."""
    return {value for value in values if values.count(value) > 1}


def validate_required_string_field(cleaned_input, field_name: str):
    """Strip and validate field value."""
    field_value = cleaned_input.get(field_name)
    field_value = field_value.strip() if field_value else ""
    if field_value:
        cleaned_input[field_name] = field_value
    else:
        raise ValidationError(f"{field_name.capitalize()} is required.")
    return cleaned_input


def list_to_queryset(data, model=None):
    from django.db.models.base import ModelBase
    if not model:
        model = type(data[0])

    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)

