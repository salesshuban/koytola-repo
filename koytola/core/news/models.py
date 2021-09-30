from django.db import models
from django.db.models import Q

from ..core.utils.editorjs import clean_editor_js
from ..core.db.fields import SanitizedJSONField
from ..core.models import PublishableModel, PublishedQuerySet
from ..core.permissions import NewsPermissions
from ..core.utils.translations import TranslationProxy
from ..seo.models import SeoModel, SeoModelTranslation
from . import NewsAudienceType


class NewsPublishedQuerySet(PublishedQuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(NewsPermissions.MANAGE_NEWS)

    def visible_to_user(self, user):
        if self.user_has_access_to_all(user):
            return self.all()
        else:
            if user.is_staff:
                qs = self.filter(
                    Q(audience=NewsAudienceType.STAFF) |
                    Q(audience=NewsAudienceType.PLATFORM) |
                    Q(audience=NewsAudienceType.PUBLIC)
                )
                return qs.filter(is_published=True)
            elif user.is_active:
                qs = self.filter(
                    Q(audience=NewsAudienceType.PLATFORM) |
                    Q(audience=NewsAudienceType.PUBLIC)
                )
                return qs.filter(is_published=True)
            else:
                return self.filter(
                    Q(audience=NewsAudienceType.PUBLIC) & Q(is_published=True)
                )

    def platform(self):
        return self.filter(
            Q(audience=NewsAudienceType.PLATFORM) & Q(is_published=True)
        )

    def public(self):
        return self.filter(
            Q(audience=NewsAudienceType.PUBLIC) & Q(is_published=True)
        )

    def staff(self):
        return self.filter(
            Q(audience=NewsAudienceType.STAFF) & Q(is_published=True)
        )


class News(PublishableModel, SeoModel):
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    summary = models.CharField(max_length=320, blank=True, null=True)
    content = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_editor_js
    )
    link = models.URLField(blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    audience = models.CharField(
        max_length=32,
        choices=NewsAudienceType.CHOICES,
        default=NewsAudienceType.OTHER
    )
    is_active = models.BooleanField(default=True)
    objects = NewsPublishedQuerySet.as_manager()
    translated = TranslationProxy()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["slug"]
        permissions = [(NewsPermissions.MANAGE_NEWS.codename, "Manage news.")]

    def __str__(self):
        return self.title


class NewsTranslation(SeoModelTranslation):
    language_code = models.CharField(max_length=10)
    news = models.ForeignKey(
        News, related_name="translations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=320, blank=True)
    content = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_editor_js
    )
    content_plaintext = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["language_code", "news", "pk"]
        unique_together = [("language_code", "news")]

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, title=%r, news_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.title,
            self.news_id,
        )

    def __str__(self):
        return self.title
