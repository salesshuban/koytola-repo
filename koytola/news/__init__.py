class NewsAudienceType:
    PUBLIC = "public"
    PLATFORM = "platform"
    STAFF = "staff"
    OTHER = "other"

    CHOICES = [
        (PUBLIC, "Represents public news or announcement"),
        (PLATFORM, "News dedicated to users in the platform"),
        (STAFF, "News for staff members"),
        (OTHER, "News for other audience type"),
    ]
