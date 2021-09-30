import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import (
    ProductBulkUpdate,
    ProductBulkDelete,
    ProductBulkPublish,
    ProductBulkUnpublish
)
from .filters import ProductFilterInput, PortDealsFilterInput
from .mutations.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
)
from .mutations.product import (
    ProductCreate,
    ProductActivate,
    ProductPublish,
    ProductUpdate,
    ProductUnpublish,
    ProductDeactivate,
    ProductDelete,
)
from .mutations.product_image import (
    ProductImageCreate,
    ProductImageUpdate,
    ProductImageDelete,
    ProductImageIndexUpdate
)
from .mutations.product_video import (
    ProductVideoCreate,
    ProductVideoUpdate,
    ProductVideoDelete,

)
from .mutations.offers import (
    OffersCreate,
    OffersUpdate,
    OfferActivate,
    OfferDeactivate,
    OfferDelete,
    OffersBulkDelete,
)
from .mutations.port_deals import (
    PortDealsCreate,
    PortDealsGalleryCreate,
    PortDealsBulkDelete,
    PortDealsUpdate,
    PortDealsGalleryDelete
)
from .mutations.product_query import (
    ProductQueryCreate
)
from .mutations.product_reviews import (
    ProductReviewsCreate
)
from .resolvers import (
    resolve_category,
    resolve_categories,
    resolve_product,
    resolve_products,
    resolve_product_image,
    resolve_product_images,
    resolve_product_video,
    resolve_product_videos,
    resolve_search_hscode_and_product,
    resolve_currency_exchange,
    resolve_offer,
    resolve_offers,
    resolve_port_deal,
    resolve_port_deals,
    resolve_search_product,
    resolve_search_port_deals,
    resolve_product_reviews,
    resolve_product_rosetters,
    resolve_product_certificate_type,
    resolve_product_queries,
    resolve_product_query,
    resolve_port_product_gallery,
    resolve_data_insert
)
from .sorters import ProductSortingInput, OfferSortingInput, ProductQuerySortingInput, PortDealsSortingInput
from .types import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    HSCodeAndProduct,
    Offers,
    PortDeals,
    PortProductGallery,
    ProductReviews,
    ProductQuery,
    OpenExchange
)
from ..profile.types import Roetter, CertificateType


class ProductQueries(graphene.ObjectType):
    product_certificate_type = graphene.List(
        CertificateType,
        description="product certificate type."
    )
    search_hscode_and_product = graphene.List(
        HSCodeAndProduct,
        key=graphene.Argument(
            graphene.String,
            description="search key of the hs code and product."
        )
    )
    search_product = FilterInputConnectionField(
        Product,
        key=graphene.String(description="search key of product"),
        description="List of categories.",
    )
    search_port_deals = FilterInputConnectionField(
        PortDeals,
        key=graphene.String(description="search key of product"),
        description="search port deals.",
    )
    category = graphene.Field(
        Category,
        category_id=graphene.Argument(
            graphene.ID, description="ID of the category."
        ),
        slug=graphene.Argument(
            graphene.String, description="name of the category."
        ),
        description="Category by ID or name.",
    )
    categories = FilterInputConnectionField(
        Category,
        description="List of categories.",
    )
    product = graphene.Field(
        Product,
        id=graphene.Argument(
            graphene.ID, description="ID of the product."
        ),
        slug=graphene.Argument(
            graphene.String, description="slug of the product."
        ),
        description="Product by ID or slug.",
    )
    products = FilterInputConnectionField(
        Product,
        filter=ProductFilterInput(description="Filtering options for products."),
        sort_by=ProductSortingInput(description="Sort products."),
        company_id=graphene.ID(required=False, description="products from company"),
        description="List of products.",
    )
    product_image = graphene.Field(
        ProductImage,
        id=graphene.Argument(
            graphene.ID, description="ID of the product image."
        ),
        description="Product image by ID.",
    )
    product_images = FilterInputConnectionField(
        ProductImage,
        product_id=graphene.Argument(
            graphene.ID, description="ID of the product for its images."
        ),
        description="Product images.",
    )
    product_video = graphene.Field(
        ProductVideo,
        id=graphene.Argument(
            graphene.ID, description="ID of the product video."
        ),
        description="Product video by ID.",
    )
    product_videos = FilterInputConnectionField(
        ProductVideo,
        product_id=graphene.Argument(
            graphene.ID, description="ID of the product for its videos."
        ),
        description="Product videos.",
    )
    product_reviews = FilterInputConnectionField(
        ProductReviews,
        product_id=graphene.Argument(
            graphene.ID, description="ID of the product for its videos."
        ),
        description="Product videos.",
    )
    currency_exchange = graphene.Field(OpenExchange, base=graphene.Argument(
        graphene.String, description="ID of the product for its videos."
    ), )

    offer = graphene.Field(
        Offers,
        id=graphene.Argument(
            graphene.ID, description="ID of the Offer."
        ),
        description="offer by ID.",
    )
    offers = FilterInputConnectionField(
        Offers,
        company_id=graphene.Argument(
            graphene.ID, description="ID of the product for its videos.", required=False
        ),
        sort_by=OfferSortingInput(description="Sort products."),
        description="List of products.",
    )
    port_deal = graphene.Field(
        PortDeals,
        id=graphene.Argument(graphene.ID, description="ID of the Offer."),
        description="offer by ID.",
    )

    port_deals = FilterInputConnectionField(
        PortDeals,
        company_id=graphene.Argument(graphene.ID, description="ID of the product for its port deals.", required=False),
        filter=PortDealsFilterInput(description="Filtering options for products."),
        sort_by=PortDealsSortingInput(description="Sort products."),
        description="offer by ID.",
    )

    product_rosetters = graphene.List(Roetter, description="List of rosetters.", )
    product_query = graphene.Field(
        ProductQuery,
        id=graphene.Argument(graphene.ID, description="ID of the Offer."),
        description="offer by ID.",
    )
    product_queries = FilterInputConnectionField(
        ProductQuery,
        company_id=graphene.Argument(graphene.ID, description="ID of the product for its port deals.", required=False),
        sort_by=ProductQuerySortingInput(description="Sort products."),
        description="offer by ID.",
    )
    port_product_gallery = FilterInputConnectionField(
        PortProductGallery,
        port_deal_id=graphene.Argument(graphene.ID, description="ID of the Offer."),
    )
    data_insert = graphene.String()

    def resolve_data_insert(self, info, **kwargs):
        return resolve_data_insert(info, **kwargs)

    def resolve_port_product_gallery(self, info, port_deal_id, **kwargs):
        return resolve_port_product_gallery(info, port_deal_id, **kwargs)

    def resolve_product_queries(self, info, company_id, **kwargs):
        return resolve_product_queries(info, company_id, **kwargs)

    def resolve_product_query(self, info, id, **kwargs):
        return resolve_product_query(info, id, **kwargs)

    def resolve_product_certificate_type(self, info, **kwargs):
        return resolve_product_certificate_type(info, **kwargs)

    def resolve_product_rosetters(self, info, **kwargs):
        return resolve_product_rosetters(info, **kwargs)

    def resolve_search_port_deals(self, info, key, **kwargs):
        return resolve_search_port_deals(info, key, **kwargs)

    def resolve_port_deal(self, info, id=None, name=None):
        return resolve_port_deal(info, id, name)

    def resolve_port_deals(self, info, company_id=None, **kwargs):
        return resolve_port_deals(info, company_id, **kwargs)

    def resolve_offer(self, info, id=None, name=None):
        return resolve_offer(info, id, name)

    def resolve_offers(self, info, company_id=None, **kwargs):
        return resolve_offers(info, company_id, **kwargs)

    def resolve_search_product(self, info, key, **kwargs):
        return resolve_search_product(info, key, **kwargs)

    def resolve_currency_exchange(self, info, base=None, **kwargs):
        return resolve_currency_exchange(info, base, **kwargs)

    def resolve_search_hscode_and_product(self, info, key=None, **kwargs):
        return resolve_search_hscode_and_product(info, key, **kwargs)

    def resolve_category(self, info, category_id=None, slug=None):
        return resolve_category(info, category_id, slug)

    def resolve_categories(self, info, query=None, **kwargs):
        return resolve_categories(info, query, **kwargs)

    def resolve_product(self, info, id=None, slug=None):
        return resolve_product(info, id, slug)

    def resolve_products(self, info, company_id=None, **kwargs):
        return resolve_products(info, company_id, **kwargs)

    def resolve_company_products(self, info, **kwargs):
        return resolve_products(info, **kwargs)

    def resolve_product_image(self, info, id=None):
        return resolve_product_image(info, id)

    def resolve_product_images(self, info, **kwargs):
        return resolve_product_images(info, **kwargs)

    def resolve_product_video(self, info, product_video_id=None):
        return resolve_product_video(info, product_video_id)

    def resolve_product_videos(self, info, **kwargs):
        return resolve_product_videos(info, **kwargs)

    def resolve_product_reviews(self, info, product_id=None, **kwargs):
        return resolve_product_reviews(info, product_id, **kwargs)


class ProductMutations(graphene.ObjectType):
    product_create = ProductCreate.Field()
    product_activate = ProductActivate.Field()
    product_publish = ProductPublish.Field()
    product_update = ProductUpdate.Field()
    product_unpublish = ProductUnpublish.Field()
    product_deactivate = ProductDeactivate.Field()
    product_delete = ProductDelete.Field()
    product_image_create = ProductImageCreate.Field()
    product_image_update = ProductImageUpdate.Field()
    product_image_delete = ProductImageDelete.Field()
    product_image_index_update = ProductImageIndexUpdate.Field()
    product_video_create = ProductVideoCreate.Field()
    product_video_update = ProductVideoUpdate.Field()
    product_video_delete = ProductVideoDelete.Field()
    product_bulk_update = ProductBulkUpdate.Field()
    product_bulk_delete = ProductBulkDelete.Field()
    product_bulk_publish = ProductBulkPublish.Field()
    product_bulk_unpublish = ProductBulkUnpublish.Field()
    offer_create = OffersCreate.Field()
    offer_update = OffersUpdate.Field()
    offer_activate = OfferActivate.Field()
    offer_deactivate = OfferDeactivate.Field()
    offer_delete = OfferDelete.Field()
    offer_bulk_delete = OffersBulkDelete.Field()
    port_deals_create = PortDealsCreate.Field()
    port_deals_bulk_delete = PortDealsBulkDelete.Field()
    port_deals_gallery_create = PortDealsGalleryCreate.Field()
    port_deals_gallery_delete = PortDealsGalleryDelete.Field()
    port_deals_update = PortDealsUpdate.Field()
    product_reviews_create = ProductReviewsCreate.Field()
    product_query_create = ProductQueryCreate.Field()
