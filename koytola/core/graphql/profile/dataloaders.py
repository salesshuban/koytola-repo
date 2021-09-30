from collections import defaultdict

from ...profile.models import (
    Brochure,
    Certificate,
    Company,
    Representative,
    SocialResponsibility,
    Video
)
from ..core.dataloaders import DataLoader


class CompanyByIdLoader(DataLoader):
    context_key = "company_by_id"

    def batch_load(self, keys):
        companies = Company.objects.in_bulk(keys)
        return [companies.get(company_id) for company_id in keys]


class BrochureByIdLoader(DataLoader):
    context_key = "brochure_by_id"

    def batch_load(self, keys):
        brochure = Brochure.objects.in_bulk(keys)
        return [brochure.get(brochure_id) for brochure_id in keys]


class BrochuresByIdLoader(DataLoader):
    context_key = "brochures_by_id"

    def batch_load(self, keys):
        brochures = Brochure.objects.filter(company_id__in=keys)
        items_map = defaultdict(list)
        for brochure in brochures.iterator():
            items_map[brochure.company_id].append(brochure)
        return [items_map[company_id] for company_id in keys]


class CertificateByIdLoader(DataLoader):
    context_key = "certificate_by_id"

    def batch_load(self, keys):
        certificate = Certificate.objects.in_bulk(keys)
        return [certificate.get(certificate_id) for certificate_id in keys]


class CertificatesByIdLoader(DataLoader):
    context_key = "certificates_by_id"

    def batch_load(self, keys):
        certificates = Certificate.objects.filter(company_id__in=keys)
        items_map = defaultdict(list)
        for certificate in certificates.iterator():
            items_map[certificate.company_id].append(certificate)
        return [items_map[company_id] for company_id in keys]


class RepresentativeByIdLoader(DataLoader):
    context_key = "representative_by_id"

    def batch_load(self, keys):
        representative = Representative.objects.in_bulk(keys)
        return [representative.get(representative_id) for representative_id in keys]


class SocialResponsibilityByIdLoader(DataLoader):
    context_key = "social_responsibility_by_id"

    def batch_load(self, keys):
        social_responsibility = SocialResponsibility.objects.in_bulk(keys)
        return [
            social_responsibility.get(social_responsibility_id)
            for social_responsibility_id in keys
        ]


class SocialResponsibilitiesByIdLoader(DataLoader):
    context_key = "social_responsibilities_by_id"

    def batch_load(self, keys):
        social_responsibilities = SocialResponsibility.objects.filter(company_id__in=keys)
        items_map = defaultdict(list)
        for social_responsibility in social_responsibilities.iterator():
            items_map[social_responsibility.company_id].append(social_responsibility)
        return [items_map[company_id] for company_id in keys]


class VideoByIdLoader(DataLoader):
    context_key = "video_by_id"

    def batch_load(self, keys):
        video = Video.objects.in_bulk(keys)
        return [video.get(video_id) for video_id in keys]


class VideosByIdLoader(DataLoader):
    context_key = "certificates_by_id"

    def batch_load(self, keys):
        videos = Video.objects.filter(company_id__in=keys)
        items_map = defaultdict(list)
        for video in videos.iterator():
            items_map[video.company_id].append(video)
        return [items_map[company_id] for company_id in keys]
