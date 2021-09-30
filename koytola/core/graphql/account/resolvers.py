from itertools import chain
from typing import Optional

import graphene
from django.contrib.auth import models as auth_models
from i18naddress import get_validation_rules

from ...account import models
from ...core.exceptions import PermissionDenied
from ...core.permissions import AccountPermissions
from ...payment import gateway
from ...payment.utils import fetch_account_id
from ..utils import format_permissions_for_display, get_user_or_app_from_context
from ..utils.filters import filter_by_query_param
from .types import AddressValidationData, ChoiceValue
from .utils import (
    get_allowed_fields_camel_case,
    get_required_fields_camel_case,
    get_user_permissions,
)

USER_SEARCH_FIELDS = (
    "email",
    "first_name",
    "last_name",
    "default_billing_address__first_name",
    "default_billing_address__last_name",
    "default_billing_address__city",
    "default_billing_address__country",
)


def resolve_accounts(info, query, **_kwargs):
    qs = models.User.objects.accounts()
    qs = filter_by_query_param(
        queryset=qs, query=query, search_fields=USER_SEARCH_FIELDS
    )
    return qs.distinct()


def resolve_users(info, query, **_kwargs):
    qs = models.User.objects.all()
    qs = filter_by_query_param(
        queryset=qs, query=query, search_fields=USER_SEARCH_FIELDS
    )
    return qs.distinct()


def resolve_permission_groups(info, **_kwargs):
    return auth_models.Group.objects.all()


def resolve_staff_users(info, query, **_kwargs):
    qs = models.User.objects.staff()
    qs = filter_by_query_param(
        queryset=qs, query=query, search_fields=USER_SEARCH_FIELDS
    )
    return qs.distinct()


def resolve_user(info, id=None):
    requester = get_user_or_app_from_context(info.context)
    if requester:
        if id:
            _model, user_pk = graphene.Node.from_global_id(id)
        else:
            user_pk = info.context.user.id
        if requester.has_perms(
            [AccountPermissions.MANAGE_STAFF, AccountPermissions.MANAGE_USERS]
        ):
            return models.User.objects.filter(pk=user_pk).first()
        if requester.has_perm(AccountPermissions.MANAGE_STAFF):
            return models.User.objects.staff().filter(pk=user_pk).first()
        if requester.has_perm(AccountPermissions.MANAGE_USERS):
            return models.User.objects.accounts().filter(pk=user_pk).first()

        user = info.context.user
        if user and not user.is_anonymous:
            user_model = models.User.objects.filter(pk=user_pk).first()
            if user.email == user_model.email:
                return user_model
    return PermissionDenied()


def resolve_address_validation_rules(
    info,
    country_code: str,
    country_area: Optional[str],
    city: Optional[str],
    city_area: Optional[str],
):

    params = {
        "country_code": country_code,
        "country_area": country_area,
        "city": city,
        "city_area": city_area,
    }
    rules = get_validation_rules(params)
    return AddressValidationData(
        country_code=rules.country_code,
        country_name=rules.country_name,
        address_format=rules.address_format,
        address_latin_format=rules.address_latin_format,
        allowed_fields=get_allowed_fields_camel_case(rules.allowed_fields),
        required_fields=get_required_fields_camel_case(rules.required_fields),
        upper_fields=rules.upper_fields,
        country_area_type=rules.country_area_type,
        country_area_choices=[
            ChoiceValue(area[0], area[1]) for area in rules.country_area_choices
        ],
        city_type=rules.city_type,
        city_choices=[ChoiceValue(area[0], area[1]) for area in rules.city_choices],
        city_area_type=rules.city_type,
        city_area_choices=[
            ChoiceValue(area[0], area[1]) for area in rules.city_area_choices
        ],
        postal_code_type=rules.postal_code_type,
        postal_code_matchers=[
            compiled.pattern for compiled in rules.postal_code_matchers
        ],
        postal_code_examples=rules.postal_code_examples,
        postal_code_prefix=rules.postal_code_prefix,
    )


def resolve_payment_sources(user: models.User):
    stored_accounts = (
        (gtw.id, fetch_account_id(user, gtw.id)) for gtw in gateway.list_gateways()
    )
    return list(
        chain(
            *[
                prepare_graphql_payment_sources_type(
                    gateway.list_payment_sources(gtw, account_id)
                )
                for gtw, account_id in stored_accounts
                if account_id is not None
            ]
        )
    )


def prepare_graphql_payment_sources_type(payment_sources):
    sources = []
    for src in payment_sources:
        sources.append(
            {
                "gateway": src.gateway,
                "credit_card_info": {
                    "last_digits": src.credit_card_info.last_4,
                    "exp_year": src.credit_card_info.exp_year,
                    "exp_month": src.credit_card_info.exp_month,
                    "brand": "",
                    "first_digits": "",
                },
            }
        )
    return sources


def resolve_address(info, id):
    user = info.context.user
    app = info.context.app
    _model, address_pk = graphene.Node.from_global_id(id)
    if app and app.has_perm(AccountPermissions.MANAGE_USERS):
        return models.Address.objects.filter(pk=address_pk).first()
    if user and not user.is_anonymous:
        return user.addresses.filter(id=address_pk).first()
    return PermissionDenied()


def resolve_permissions(root: models.User):
    permissions = get_user_permissions(root)
    permissions = permissions.order_by("codename")
    return format_permissions_for_display(permissions)


def resolve_account_events(info, id=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if not id:
            if user.has_perms([AccountPermissions.MANAGE_STAFF]) \
              and user.has_perms([AccountPermissions.MANAGE_USERS]):
                return models.AccountEvent.objects.all()
            elif user.has_perms([AccountPermissions.MANAGE_STAFF]):
                return models.AccountEvent.objects.filter(user__is_staff=True)
            elif user.has_perms([AccountPermissions.MANAGE_USERS]):
                return models.AccountEvent.objects.filter(user__is_staff=False)
        else:
            model, account = graphene.Node.from_global_id(id)
            if user == account:
                return models.AccountEvent.objects.filter(user=user)
    raise PermissionDenied()


def resolve_countries(info, **_kwargs):
    return models.Countries.objects.filter()
