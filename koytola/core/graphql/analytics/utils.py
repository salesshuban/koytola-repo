from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Model
from geolite2 import geolite2
from typing import Type
from user_agents import parse

from ...analytics.error_codes import TrackingErrorCode
from ...analytics.models import Tracking
from ...analytics import TrackingTypes
from ...core.utils import (
    _get_geo_data_by_ip,
    get_client_ip,
)


georeader = geolite2.reader()


def save_request_data(info, args=dict):
    meta = info.context.META
    ip = get_client_ip(info.context)
    ua_data = parse(meta["HTTP_USER_AGENT"])
    device_type = get_device_type(ua_data)
    
    tracking = Tracking.objects.create(
        ip=ip,
        referrer=meta["HTTP_REFERER"],
        device_type=device_type,
        device=ua_data.device.family,
        browser=ua_data.browser.family,
        browser_version=ua_data.browser.version_string,
        system=ua_data.os.family,
        system_version=ua_data.os.version_string,
    )

    if info.context.user:
        tracking.user_id = info.context.user.pk

    try:
        if ip and ip not in settings.INTERNAL_IPS:
            geo_data = get_geo_details_from_ip(ip)
            tracking.country = geo_data["country"]
            tracking.region = geo_data["region"]
            tracking.city = geo_data["city"]
            tracking.postal = geo_data["postal"],
            tracking.location_details = geo_data["location_details"],
    except Exception:
        print(Exception)

    if "category_pk" in args and args["category_pk"]:
        tracking.category_id = args["category_pk"]
        tracking.type = TrackingTypes.CATEGORY
    if "company_pk" in args and args["company_pk"]:
        tracking.company_id = args["company_pk"]
        tracking.type = TrackingTypes.COMPANY
    if "product_pk" in args and args["product_pk"]:
        tracking.product_id = args["product_pk"]
        tracking.type = TrackingTypes.PRODUCT

    tracking.save()


def get_geo_details_from_ip(ip):
    geo_data = _get_geo_data_by_ip(ip)
    if geo_data:
        return {
            "city": geo_data["city"]["names"]["en"] if "city" in geo_data else "",
            "region": geo_data["subdivisions"][0]["names"]["en"] if "subdivisions" in geo_data else "",
            "country": geo_data["country"]["iso_code"] if "country" in geo_data else "",
            "postal": geo_data["postal"]["code"] if "postal" in geo_data else "",
            "location_details": geo_data["location"] if "location" in geo_data else "",
        }
    else:
        return None


def get_device_type(data):
    if data.is_bot:
        device_type = "Bot"
    elif data.is_email_client:
        device_type = "Email Client"
    elif data.is_mobile:
        device_type = "Mobile"
    elif data.is_pc:
        device_type = "PC"
    elif data.is_tablet:
        device_type = "Tablet"
    elif data.is_touch_capable:
        device_type = "Touch Device"
    else:
        device_type = "Unknown"
    return device_type


def validate_tracking_instance(
    cleaned_input: dict, field: str, expected_model: Type[Model]
):
    """Check if the value to assign as a tracking matches the expected model."""
    item = cleaned_input.get(field)
    if item:
        if not isinstance(item, expected_model):
            msg = (
                f"Enter a valid {expected_model._meta.verbose_name} ID "
                f"(got {item._meta.verbose_name} ID)."
            )
            raise ValidationError(
                {
                    field: ValidationError(
                        msg, code=TrackingErrorCode.INVALID.value
                    )
                }
            )
