class CompanySize:
    """Company type on the platform."""

    NONE = "none"
    SMALL_BUSINESS = "small_business"
    MEDIUM_BUSINESS = "medium_business"
    LARGE_ENTERPRISE = "large_enterprise"

    CHOICES = [
        (NONE, "No company size is chosen"),
        (SMALL_BUSINESS, "Small business"),
        (MEDIUM_BUSINESS, "Medium size business"),
        (LARGE_ENTERPRISE, "Large enterprise"),
    ]


class CompanyType:
    """Company type on the platform."""

    MANUFACTURER = "manufacturer"
    SUPPLIER = "supplier"

    CHOICES = [
        (MANUFACTURER, "Manufacturer company type"),
        (SUPPLIER, "Supplier company type"),
    ]


class EmployeeNumber:
    """Company employee number levels similar to Linkedin."""

    CHOICES = [
        ("1-10", "1-10"),
        ("11-50", "11-50"),
        ("51-200", "51-200"),
        ("201-500", "201-500"),
        ("501-1000", "501-1000"),
        ("1001-5000", "1001-5000"),
        ("5001-10,000", "5001-10,000"),
        ("10,000+", "10,000+"),
    ]


class TrackingTypes:
    """The tracking types."""

    OTHER = "other"
    PROFILE = "profile"
    PROFILE_LINK = "profile_link"
    PROFILE_SOCIAL = "profile_social"
    PROFILE_WEBSITE = "profile_website"
    URL_SHORTENER = "url_shortener"

    CHOICES = [
        (OTHER, "Other type of click tracking"),
        (PROFILE, "Profile visit tracking"),
        (PROFILE_LINK, "Profile Link click tracking"),
        (PROFILE_SOCIAL, "Profile Social click tracking"),
        (PROFILE_WEBSITE, "Profile Website click tracking"),
        (URL_SHORTENER, "Url Shortener click tracking"),
    ]


class MessageType:
    """Company contact message types."""

    INFO = "info"
    QUOTATION = "quotation"
    OTHER = "other"

    CHOICES = [
        (INFO, "Info message type"),
        (QUOTATION, "Quotation message type"),
        (OTHER, "Other message type"),
    ]


class MessageStatus:
    """Company contact message status."""

    NEW = "new"
    ONGOING = "ongoing"
    DONE = "done"
    SPAM = "spam"

    CHOICES = [
        (NEW, "New message"),
        (ONGOING, "Message status is ongoing"),
        (DONE, "Message is done"),
        (SPAM, "Message marked as spam"),
    ]
