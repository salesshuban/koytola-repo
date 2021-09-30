from graphene_federation import build_schema

from .account.schema import AccountMutations, AccountQueries
from .analytics.schema import AnalyticsMutations, AnalyticsQueries
from .app.schema import AppMutations, AppQueries
from .blog.schema import BlogMutations, BlogQueries
from .core.schema import CoreQueries
from .helpdesk.schema import HelpdeskQueries, HelpdeskMutations
from .invoice.schema import InvoiceMutations
from .menu.schema import MenuQueries, MenuMutations
from .meta.schema import MetaMutations
from .news.schema import NewsQueries, NewsMutations
from .order.schema import OrderQueries, OrderMutations
from .page.schema import PageMutations, PageQueries
from .payment.schema import PaymentMutations, PaymentQueries
from .plugins.schema import PluginsMutations, PluginsQueries
from .product.schema import ProductMutations, ProductQueries
from .profile.schema import ProfileMutations, ProfileQueries
from .site.schema import SiteMutations, SiteQueries
from .translations.schema import TranslationQueries
from .webhook.schema import WebhookMutations, WebhookQueries


class Query(
    AccountQueries,
    AnalyticsQueries,
    AppQueries,
    BlogQueries,
    CoreQueries,
    HelpdeskQueries,
    PluginsQueries,
    MenuQueries,
    NewsQueries,
    OrderQueries,
    PageQueries,
    PaymentQueries,
    ProductQueries,
    ProfileQueries,
    SiteQueries,
    TranslationQueries,
    WebhookQueries,
):
    pass


class Mutation(
    AccountMutations,
    AnalyticsMutations,
    AppMutations,
    BlogMutations,
    PluginsMutations,
    HelpdeskMutations,
    InvoiceMutations,
    MenuMutations,
    MetaMutations,
    NewsMutations,
    OrderMutations,
    PageMutations,
    PaymentMutations,
    ProductMutations,
    ProfileMutations,
    SiteMutations,
    WebhookMutations
):
    pass


schema = build_schema(Query, mutation=Mutation)
