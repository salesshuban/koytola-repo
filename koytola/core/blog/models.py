from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField
from ..core.db.fields import SanitizedJSONField
from ..core.models import PublishableModel, PublishedQuerySet, ModelWithMetadata
from ..core.permissions import BlogPermissions
from ..core.utils.editorjs import clean_editor_js
from ..core.utils.translations import TranslationProxy
from ..seo.models import SeoModel, SeoModelTranslation
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from ..core.utils import upload_path_handler
from ..account.models import User


class BlogPublishedQuerySet(PublishedQuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(BlogPermissions.MANAGE_BLOGS)


class BlogCategory(MPTTModel, ModelWithMetadata, SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    description_plaintext = models.TextField(blank=True, default="")
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = VersatileImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    objects = models.Manager()
    tree = TreeManager()
    tags = models.TextField(max_length=25000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ["slug", "name", "pk"]
        permissions = [
            (
                BlogPermissions.MANAGE_BLOG_CATEGORIES.codename,
                "Manage Blog categories."
            )
        ]

    def __str__(self) -> str:
        return self.name


class Blog(SeoModel, PublishableModel):
    category = models.ManyToManyField(BlogCategory, related_name="blog_category", blank=True)
    user = models.ForeignKey(User, related_name="blog_user", on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    short_description = models.TextField(max_length=65500, blank=True, null=True)
    description = models.TextField(max_length=65500, blank=True, null=True)
    tags = models.TextField(max_length=65500, blank=True, default="[]")
    objects = BlogPublishedQuerySet.as_manager()
    translated = TranslationProxy()
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["slug"]
        permissions = [(BlogPermissions.MANAGE_BLOGS.codename, "Manage blogs.")]

    def __str__(self):
        return self.title


class BlogTranslation(SeoModelTranslation):
    language_code = models.CharField(max_length=10)
    blog = models.ForeignKey(
        Blog, related_name="translations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=320, blank=True)
    content = SanitizedJSONField(blank=True, default=dict, sanitizer=clean_editor_js)
    content_plaintext = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["language_code", "blog", "pk"]
        unique_together = [("language_code", "blog")]

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, title=%r, blog_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.title,
            self.blog_id,
        )

    def __str__(self):
        return self.title
