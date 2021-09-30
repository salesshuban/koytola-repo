from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from ....site.models import SiteSettings


class Command(BaseCommand):
    help = "Creates SiteSettings model data from the database for initial site configuration."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allows running the cleardb command in DEBUG=False mode.",
        )

    def handle(self, **options):
        force = options.get("force", False)
        if not settings.DEBUG and not force:
            raise CommandError("Cannot generate the site settings in DEBUG=False mode.")

        site = Site.objects.all().first()
        if not site:
            site = Site.objects.create(
                name="Project Site",
                domain="localhost:8000"
            )

        site_settings = SiteSettings.objects.all().first()
        if not site_settings:
            SiteSettings.objects.create(
                site=site,
                description="Site description",
                header_text="Site Header Text"
            )
