from django.core.exceptions import ValidationError
from django.db.models import Q

from ...core.exceptions import PermissionDenied
from ...core.permissions import ProfilePermissions
from ...profile import models
from ...profile.error_codes import ProfileErrorCode


def company_permission(info, company):
    # Raise error if the current user doesn't have permission.
    if company.user and company.user != info.context.user or not company.user.is_seller:
        if not info.context.user.has_perm(
                ProfilePermissions.MANAGE_PROFILES
        ):
            raise PermissionDenied()

    # Raise error if the company status is inactive.
    if not company.is_active:
        if not info.context.user.has_perm(ProfilePermissions.MANAGE_PROFILES):
            raise PermissionDenied()


def company_address_permission(info, address):
    # Raise error if the current user doesn't have permission.
    company = models.Company.objects.filter(address_id=address.id).first()
    if company.user and company.user != info.context.user:
        if not info.context.user.has_perm(
                ProfilePermissions.MANAGE_PROFILES
        ):
            raise PermissionDenied()

    # Raise error if the company status is inactive.
    if not company.is_active:
        if not info.context.user.has_perm(ProfilePermissions.MANAGE_PROFILES):
            raise PermissionDenied()


def clean_company_slug(info, data=None):
    # Validate company slug and raise error if it is already taken.
    if data:
        if hasattr(data, "slug"):
            slug = data.get("slug")
            company = models.Company.objects.filter(slug=slug).first()
            if company and company.user != info.context.user:
                msg = "This slug is already taken."
                code = ProfileErrorCode.SLUG_TAKEN.value
                raise ValidationError({"id": ValidationError(msg, code=code)})
        if hasattr(data, "input") and hasattr(data.get("input"), "slug"):
            slug = data["input"]["username"]
            company = models.Company.objects.filter(slug=slug).first()
            if company and company.user != info.context.user:
                msg = "This slug is already taken."
                code = ProfileErrorCode.SLUG_TAKEN.value
                raise ValidationError({"id": ValidationError(msg, code=code)})


def contact_filter(data):
    # Raise error if contact sender has already too many pending requests.
    if len(models.Contact.objects.filter(
            Q(email=data.get("input")["email"]) & Q(status__iexact="New")
    )) > 5 or len(models.Contact.objects.filter(
        Q(email=data.get("input")["email"]) & Q(status__iexact="Spam")
    )) > 5:
        msg = "You have too many messages pending."
        code = ProfileErrorCode.CONTACT_FILTER.value
        raise ValidationError({"id": ValidationError(msg, code=code)})

