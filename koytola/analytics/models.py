from django.db import models
from django.db.models import JSONField  # type: ignore
from django.utils import timezone

from ..core.permissions import AnalyticsPermissions
from ..core.utils.json_serializer import CustomJsonEncoder
from ..core.models import ModelWithMetadata
from . import TrackingTypes


class Tracking(ModelWithMetadata):
    """Model used to store tracking details."""

    user = models.ForeignKey(
        "account.User",
        related_name="analytics",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    date = models.DateTimeField(default=timezone.now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in TrackingTypes.CHOICES
        ],
        default=TrackingTypes.OTHER
    )
    category = models.ForeignKey(
        "product.Category", on_delete=models.SET_NULL, blank=True, null=True
    )
    company = models.ForeignKey(
        "profile.Company", on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.SET_NULL, blank=True, null=True
    )

    # Tracking Details
    ip = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal = models.CharField(max_length=255, blank=True)
    location_details = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)
    referrer = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=255, blank=True)
    device = models.CharField(max_length=30, blank=True)
    browser = models.CharField(max_length=30, blank=True)
    browser_version = models.CharField(max_length=30, blank=True)
    system = models.CharField(max_length=30, blank=True)
    system_version = models.CharField(max_length=30, blank=True)

    # Other Parameters
    parameters = JSONField(blank=True, default=dict, encoder=CustomJsonEncoder)

    class Meta:
        ordering = ["-date"]
        permissions = (
            (AnalyticsPermissions.MANAGE_TRACKING.codename, "Manage tracking."),
        )
