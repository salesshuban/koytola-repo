class TrackingTypes:
    """The tracking types."""

    OTHER = "other"
    CATEGORY = "category"
    COMPANY = "company"
    PRODUCT = "product"

    CHOICES = [
        (OTHER, "Other type of click tracking"),
        (CATEGORY, "category visit tracking"),
        (COMPANY, "company visit tracking"),
        (PRODUCT, "product visit tracking"),
    ]
