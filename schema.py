import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import (
    CompanyBulkUpdate,
    CompanyBulkDelete
)
from .filters import CompanyFilterInput, SuccessStoryFilterInput
from .mutations.company import (
    CompanyCreate,
    CompanyActivate,
    CompanyPublish,
    CompanyUpdate,
    CompanyUpdateAdmin,
    CompanyUnpublish,
    CompanyDeactivate,
    CompanyDelete,
    CompanyAddressCreate,
    CompanyAddressUpdate,
    CompanyAddressDelete,
)
from .mutations.success_story import *
from .mutations.representative import (
    RepresentativeCreate,
    RepresentativeUpdate,
    RepresentativeDelete,
)
from .mutations.certificate import (
    CertificateCreate,
    CertificateUpdate,
    CertificateDelete,
)
from .mutations.brochure import (
    BrochureCreate,
    BrochureUpdate,
    BrochureDelete,
)
from .mutations.images import (
    ImageCreate,
    ImageUpdate,
    ImageDelete,
)
from .mutations.video import (
    VideoCreate,
    VideoUpdate,
    VideoDelete,
)
from .mutations.social_responsibility import (
    SocialResponsibilityCreate,
    SocialResponsibilityUpdate,
    SocialResponsibilityDelete,
)
from .mutations.contact import (
    ContactCreate,
    ContactUpdate,
    ContactDelete,
    ContactBulkDelete
)
from .mutations.trade_show import (
    TradeShowCreate
)
from .resolvers import (
    resolve_company,
    resolve_companies,
    resolve_user_company,
    resolve_user_companies,
    resolve_representative,
    resolve_representatives,
    resolve_certificate,
    resolve_certificates,
    resolve_brochure,
    resolve_brochures,
    resolve_video,
    resolve_videos,
    resolve_social_responsibility,
    resolve_social_responsibilities,
    resolve_contact,
    resolve_contacts,
    resolve_images,
    resolve_image,
    resolve_industries,
    resolve_certificate_type,
    resolve_industry,
    resolve_success_story,
    resolve_success_stories,
    resolve_company_rosetters,
    resolve_trade_shows,
    resolve_trade_show
)
from .sorters import CompanySortingInput, ContactsSortingInput, SuccessStorySortingInput, SocialResponsibilitySortingInput, TradeShowsInput
from .types import (
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
    TradeShow
)


class ProfileQueries(graphene.ObjectType):
    industry = graphene.Field(
        Industry,
        id=graphene.Argument(
            graphene.ID, description="ID of the industry."
        ),
        description="List of company industry."
    )
    industries = graphene.List(
        Industry,
        description="List of company industries."
    )
    certificate_type = graphene.List(
        CertificateType,
        description="List of company industries."
    )
    company = graphene.Field(
        Company,
        id=graphene.Argument(
            graphene.ID, description="ID of the company."
        ),
        slug=graphene.Argument(
            graphene.String, description="slug of the company."
        ),
        description="Company by ID or slug.",
    )
    companies = FilterInputConnectionField(
        Company,
        filter=CompanyFilterInput(description="Filtering options for companies."),
        sort_by=CompanySortingInput(description="Sort companies."),
        description="List of companies.",
    )
    user_company = graphene.Field(
        Company,
        description="User company profiles.",
    )
    user_companies = graphene.List(
        Company,
        description="List of user company profiles.",
    )
    representative = graphene.Field(
        Representative,
        id=graphene.Argument(
            graphene.ID, description="ID of the company representative."
        ),
        description="Company representative by ID.",
    )
    representatives = FilterInputConnectionField(
        Representative,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the profile for its representative."
        ),
        description="List of company representatives.",
    )
    certificate = graphene.Field(
        Certificate,
        id=graphene.Argument(graphene.ID, description="ID of the company certificate."),
        description="Company certificate by ID.",
    )
    certificates = FilterInputConnectionField(
        Certificate,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its certificates."
        ),
        description="List of company certificates.",
    )
    brochure = graphene.Field(
        Brochure,
        id=graphene.Argument(
            graphene.ID, description="ID of the company brochure."
        ),
        description="Company brochure by ID.",
    )
    brochures = FilterInputConnectionField(
        Brochure,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its brochures."
        ),
        description="List of company brochures.",
    )
    image = graphene.Field(
        Images,
        id=graphene.Argument(
            graphene.ID, description="ID of the company image."
        ),
        description="Company image by ID.",
    )
    images = FilterInputConnectionField(
        Images,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its images."
        ),
        description="List of company images.",
    )
    video = graphene.Field(
        Video,
        id=graphene.Argument(
            graphene.ID, description="ID of the company video."
        ),
        description="Company video by ID.",
    )
    videos = FilterInputConnectionField(
        Video,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its videos."
        ),
        description="List of company videos.",
    )
    social_responsibility = graphene.Field(
        SocialResponsibility,
        id=graphene.Argument(
            graphene.ID, description="ID of the company social responsibility."
        ),
        description="Company social responsibility by ID.",
    )
    social_responsibilities = FilterInputConnectionField(
        SocialResponsibility,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its social responsibilities."
        ),
        sort_by=SocialResponsibilitySortingInput(description="Sort pages."),
        description="List of company social responsibilities.",
    )
    contact = graphene.Field(
        Contact,
        id=graphene.Argument(
            graphene.ID, description="ID of the contact."
        ),
        description="Contact by ID.",
    )
    contacts = FilterInputConnectionField(
        Contact,
        sort_by=ContactsSortingInput(description="Sort pages."),
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its contacts."
        ),
        description="List of contacts.",
    )
    success_story = graphene.Field(
        SuccessStory,
        id=graphene.Argument(
            graphene.ID, description="ID of the success story."
        ),
        description="success story by ID.",
    )
    success_stories = FilterInputConnectionField(
        SuccessStory,
        sort_by=SuccessStorySortingInput(description="Sort pages."),
        filter=SuccessStoryFilterInput(description="Filtering options for companies."),
        description="List of success stories.",
    )
    company_rosetters = graphene.List(Roetter, description="List of rosetters.",)
    trade_shows = FilterInputConnectionField(
        TradeShow,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the company for its contacts."
        ),
        sort_by=TradeShowsInput(description="Sort pages."),
        description="List of success stories.",
    )
    trade_show = graphene.Field(
        TradeShow,
        id=graphene.Argument(
            graphene.ID, description="ID of the success story."
        ),
        description="success story by ID.",
    )

    def resolve_trade_shows(self, info, **kwargs):
        return resolve_trade_shows(info, **kwargs)

    def resolve_trade_show(self, info, **kwargs):
        return resolve_trade_show(info, **kwargs)

    def resolve_company_rosetters(self, info, **kwargs):
        return resolve_company_rosetters(info, **kwargs)

    def resolve_success_story(self, info, id=None):
        return resolve_success_story(info, id)

    def resolve_success_stories(self, info, **kwargs):
        return resolve_success_stories(info, **kwargs)
    
    def resolve_industry(self, info, id=None):
        return resolve_industry(info, id)

    def resolve_industries(self, info, **kwargs):
        return resolve_industries(info, **kwargs)

    def resolve_certificate_type(self, info, **kwargs):
        return resolve_certificate_type(info, **kwargs)

    def resolve_company(self, info, id=None, slug=None):
        return resolve_company(info, id, slug)

    def resolve_companies(self, info, **kwargs):
        return resolve_companies(info, **kwargs)

    def resolve_user_company(self, info):
        from ...core.utils.random_data import create_sheet_companies
        create_sheet_companies()
        return resolve_user_company(info)

    def resolve_user_companies(self, info):
        return resolve_user_companies(info)

    def resolve_representative(self, info, id=None):
        return resolve_representative(info, id)

    def resolve_representatives(self, info, **kwargs):
        return resolve_representatives(info, **kwargs)

    def resolve_certificate(self, info, id=None):
        return resolve_certificate(info, id)

    def resolve_certificates(self, info, **kwargs):
        return resolve_certificates(info, **kwargs)

    def resolve_brochure(self, info, id=None):
        return resolve_brochure(info, id)

    def resolve_brochures(self, info, **kwargs):
        return resolve_brochures(info, **kwargs)

    def resolve_image(self, info, id=None):
        return resolve_image(info, id)

    def resolve_images(self, info, **kwargs):
        return resolve_images(info, **kwargs)

    def resolve_video(self, info, id=None):
        return resolve_video(info, id)

    def resolve_videos(self, info, **kwargs):
        return resolve_videos(info, **kwargs)

    def resolve_social_responsibility(self, info, id=None):
        return resolve_social_responsibility(info, id)

    def resolve_social_responsibilities(self, info, **kwargs):
        return resolve_social_responsibilities(info, **kwargs)

    def resolve_contact(self, info, id=None):
        return resolve_contact(info, id)

    def resolve_contacts(self, info, **kwargs):
        return resolve_contacts(info, **kwargs)


class ProfileMutations(graphene.ObjectType):
    company_create = CompanyCreate.Field()
    company_activate = CompanyActivate.Field()
    company_publish = CompanyPublish.Field()
    company_update = CompanyUpdate.Field()
    company_update_admin = CompanyUpdateAdmin.Field()
    company_unpublish = CompanyUnpublish.Field()
    company_deactivate = CompanyDeactivate.Field()
    company_delete = CompanyDelete.Field()
    company_address_create = CompanyAddressCreate.Field()
    company_address_update = CompanyAddressUpdate.Field()
    company_address_delete = CompanyAddressDelete.Field()
    representative_create = RepresentativeCreate.Field()
    representative_update = RepresentativeUpdate.Field()
    representative_delete = RepresentativeDelete.Field()
    certificate_create = CertificateCreate.Field()
    certificate_update = CertificateUpdate.Field()
    certificate_delete = CertificateDelete.Field()
    brochure_create = BrochureCreate.Field()
    brochure_update = BrochureUpdate.Field()
    brochure_delete = BrochureDelete.Field()
    image_create = ImageCreate.Field()
    image_update = ImageUpdate.Field()
    image_delete = ImageDelete.Field()
    video_create = VideoCreate.Field()
    video_update = VideoUpdate.Field()
    video_delete = VideoDelete.Field()
    social_responsibility_create = SocialResponsibilityCreate.Field()
    social_responsibility_update = SocialResponsibilityUpdate.Field()
    social_responsibility_delete = SocialResponsibilityDelete.Field()
    contact_create = ContactCreate.Field()
    contact_update = ContactUpdate.Field()
    contact_delete = ContactDelete.Field()
    contact_bulk_delete = ContactBulkDelete.Field()
    company_bulk_update = CompanyBulkUpdate.Field()
    company_bulk_delete = CompanyBulkDelete.Field()
    success_story_create = SuccessStoryCreate.Field()
    success_story_update = SuccessStoryUpdate.Field()
    success_story_activate = SuccessStoryActivate.Field()
    success_story_deactivate = SuccessStoryDeactivate.Field()
    success_story_delete = SuccessStoryDelete.Field()
    trade_show_create = TradeShowCreate.Field()
