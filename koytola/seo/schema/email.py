import json
from typing import TYPE_CHECKING

from django.contrib.sites.models import Site

from ...core.utils.json_serializer import HTMLSafeJSON

if TYPE_CHECKING:
    from ...order.models import Order


def get_organization():
    site = Site.objects.get_current()
    return {"@type": "Organization", "name": site.name}


def get_order_confirmation_markup(order: "Order") -> str:
    """Generate schema.org markup for order confirmation e-mail message."""
    organization = get_organization()
    data = {
        "@context": "http://schema.org",
        "@type": "Order",
        "merchant": organization,
        "orderNumber": order.pk,
        "priceCurrency": order.total.gross.currency,
        "price": order.total.gross.amount,
        "acceptedOffer": [],
        "orderStatus": "http://schema.org/OrderProcessing",
        "orderDate": order.created,
    }
    return json.dumps(data, cls=HTMLSafeJSON)
