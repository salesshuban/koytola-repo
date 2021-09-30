import graphene
from django.db.models import Q

from ...profile.models import (
    Company,
    Representative,
    Certificate,
    Brochure,
    Video,
    SocialResponsibility,
    Contact,
    Images,
    Industry,
    CertificateType,
    SuccessStory,
    Roetter,
    TradeShow,
)
from ...core.exceptions import PermissionDenied
from ...core.permissions import ProfilePermissions


def resolve_company(info, id=None, slug=None):
    assert id or slug, "No company ID or slug provided."
    user = info.context.user
    if slug is not None:
        return Company.objects.filter(
            Q(slug=slug) & Q(is_active=True)
        ).first()
    else:
        _model, company_pk = graphene.Node.from_global_id(id)
        if id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Company.objects.filter(pk=company_pk).first()
            else:
                company = Company.objects.filter(Q(user=user) & Q(pk=company_pk)).first()
                if company:
                    return company
    raise PermissionDenied()


def resolve_industry(info, industry_id=None):
    assert industry_id, "No industry ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, industry_pk = graphene.Node.from_global_id(industry_id)
        if industry_id is not None:
            return Industry.objects.filter(pk=industry_pk).first()
    raise PermissionDenied()


def resolve_success_story(info, success_story_id=None):
    assert success_story_id, "No Success Story ID provided."
    _model, success_story_pk = graphene.Node.from_global_id(success_story_id)
    if success_story_id is not None:
        return SuccessStory.objects.filter(pk=success_story_pk).first()
    else:
        raise PermissionDenied()


def resolve_trade_show(info, trade_show_id=None):
    assert trade_show_id, "No Success Story ID provided."
    _model, trade_show_pk = graphene.Node.from_global_id(trade_show_id)
    if trade_show_id is not None:
        return TradeShow.objects.filter(pk=trade_show_pk).first()
    else:
        raise PermissionDenied()


def resolve_success_stories(info, **kwargs):
    return SuccessStory.objects.filter(is_active=True).order_by("-created_at")


def resolve_industries(info, **kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return Industry.objects.filter(is_active=True).order_by("name")
    raise PermissionDenied()


def resolve_certificate_type(info, **kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return CertificateType.objects.filter(type="Company", is_active=True).order_by("name")
    raise PermissionDenied()


def resolve_companies(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
            return Company.objects.filter(user__is_seller=True).order_by("-creation_date")
        else:
            return Company.objects.filter(user=user).order_by("slug")
    return Company.objects.filter(Q(is_active=True) & Q(is_published=True)).order_by("name")
    # raise PermissionDenied()


def resolve_user_company(info, **_kwargs):
    user = info.context.user

    if user and not user.is_anonymous:
        companies = Company.objects.filter(Q(user=user) & Q(is_active=True)).order_by("slug")
        return companies.first()
    raise PermissionDenied()


def resolve_user_companies(info, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return Company.objects.filter(Q(user=user) & Q(is_active=True)).order_by("slug")
    raise PermissionDenied()


def resolve_representative(info, representative_id=None):
    assert representative_id, "No representative ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, representative_pk = graphene.Node.from_global_id(representative_id)
        if representative_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Representative.objects.filter(pk=representative_pk).first()
            else:
                representative = Representative.objects.filter(pk=representative_pk).first()
                if representative.company.user == user:
                    return representative
    raise PermissionDenied()


def resolve_representatives(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not company_id:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Representative.objects.all().order_by("name")
        else:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Representative.objects.all().order_by("name")
            else:
                model, company_pk = graphene.Node.from_global_id(company_id)
                company = Company.objects.filter(Q(user=user) & Q(pk=company_pk)).first()
                if company:
                    return company.representative
    raise PermissionDenied()


def resolve_certificate(info, certificate_id=None):
    assert certificate_id, "No certificate ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, certificate_pk = graphene.Node.from_global_id(certificate_id)
        if certificate_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Certificate.objects.filter(pk=certificate_pk).first()
            else:
                certificate = Certificate.objects.filter(pk=certificate_pk).first()
                if certificate.company.user == user:
                    return certificate
    raise PermissionDenied()


def resolve_certificates(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        company = Company.objects.filter(pk=company_pk, certificates__isnull=False).first()
        if company:
            return company.certificates
    raise PermissionDenied()


def resolve_brochure(info, brochure_id=None):
    assert brochure_id, "No brochure ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, brochure_pk = graphene.Node.from_global_id(brochure_id)
        if brochure_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Brochure.objects.filter(pk=brochure_pk).first()
            else:
                brochure = Brochure.objects.filter(pk=brochure_pk).first()
                if brochure.company.user == user:
                    return brochure
    raise PermissionDenied()


def resolve_image(info, image_id=None):
    assert image_id, "No image ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, image_pk = graphene.Node.from_global_id(image_id)
        if image_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Images.objects.filter(pk=image_pk).first()
            else:
                image = Images.objects.filter(pk=image_pk).first()
                if image.company.user == user:
                    return image
    raise PermissionDenied()


def resolve_brochures(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        company = Company.objects.filter(pk=company_pk, brochures__isnull=False).first()
        if company:
            return company.brochures
    raise PermissionDenied()


def resolve_images(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    print("user --- ", user)
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        company = Company.objects.filter(pk=company_pk).first()
        return company.images
    raise PermissionDenied()


def resolve_video(info, video_id=None):
    assert video_id, "No video ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, video_pk = graphene.Node.from_global_id(video_id)
        if video_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Video.objects.filter(pk=video_pk).first()
            else:
                video = Video.objects.filter(pk=video_pk).first()
                if video.company.user == user:
                    return video
    raise PermissionDenied()


def resolve_videos(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        company = Company.objects.filter(pk=company_pk, videos__isnull=False).first()
        if company:
            return company.videos
    raise PermissionDenied()


def resolve_social_responsibility(info, social_responsibility_id=None):
    assert social_responsibility_id, "No social_responsibility ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, social_responsibility_pk = graphene.Node.from_global_id(social_responsibility_id)
        if social_responsibility_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return SocialResponsibility.objects.filter(pk=social_responsibility_pk).first()
            else:
                social_responsibility = SocialResponsibility.objects.filter(pk=social_responsibility_pk).first()
                if social_responsibility.company.user == user:
                    return social_responsibility
    raise PermissionDenied()


def resolve_social_responsibilities(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        Social_responsibility = SocialResponsibility.objects.filter(company__pk=company_pk)
        return Social_responsibility
    raise PermissionDenied()


def resolve_contact(info, contact_id=None):
    assert contact_id, "No contact ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, contact_pk = graphene.Node.from_global_id(contact_id)
        if contact_id is not None:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Contact.objects.filter(pk=contact_pk).first()
            else:
                contact = Contact.objects.filter(pk=contact_pk).first()
                if contact.company.user == user:
                    return contact
    raise PermissionDenied()


def resolve_contacts(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not company_id:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Contact.objects.all().order_by("-submission_date")
        else:
            if user.has_perms([ProfilePermissions.MANAGE_PROFILES]):
                return Contact.objects.all().order_by("-submission_date")
            else:
                model, company_pk = graphene.Node.from_global_id(company_id)
                return Contact.objects.filter(company__pk=company_pk)
    raise PermissionDenied()


def resolve_trade_shows(info, **_kwargs):
    company_id = _kwargs.get("company_id")
    user = info.context.user
    if user and not user.is_anonymous:
        model, company_pk = graphene.Node.from_global_id(company_id)
        return TradeShow.objects.filter(company__pk=company_pk)
    raise PermissionDenied()


def resolve_company_rosetters(info, **_kwargs):
    return Roetter.objects.filter(type="Company", is_active=True)
