class AuthenticationBackends:
    GOOGLE = "google-oauth2"
    FACEBOOK = "facebook"

    BACKENDS = ((FACEBOOK, "Facebook-Oauth2"), (GOOGLE, "Google-Oauth2"))


class ContactMessageStatus:
    NEW = "new"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    SPAM = "spam"
    OTHER = "other"

    CHOICES = [
        (NEW, "New sent message"),
        (ONGOING, "Ongoing message status"),
        (COMPLETED, "Message status is completed"),
        (SPAM, "Message status is spam"),
        (OTHER, "Message status is other"),
    ]
