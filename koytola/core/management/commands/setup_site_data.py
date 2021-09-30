from io import StringIO

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from ....account.utils import create_superuser
from ...utils.random_data import (
    add_address_to_admin,
    create_permission_groups,
    create_staffs,
    create_hscode_and_product,
    create_sheet_companies,
    create_product_categories,
    create_countries,
    create_countries_flag,
    create_rosetter,
    create_industry,
    create_product_certificate,
    create_company_certificate
)


class Command(BaseCommand):
    help = "Setup site data"
    placeholders_dir = "koytola/static/placeholders/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--createsuperuser",
            action="store_true",
            dest="createsuperuser",
            default=False,
            help="Create admin account",
        )
        parser.add_argument(
            "--withoutimages",
            action="store_true",
            dest="withoutimages",
            default=False,
            help="Don't create product images",
        )

    def make_database_faster(self):
        """Sacrifice some of the safeguards of sqlite3 for speed.

        Users are not likely to run this command in a production environment.
        They are even less likely to run it in production while using sqlite3.
        """
        if "sqlite3" in connection.settings_dict["ENGINE"]:
            cursor = connection.cursor()
            cursor.execute("PRAGMA temp_store = MEMORY;")
            cursor.execute("PRAGMA synchronous = OFF;")

    def sequence_reset(self):
        """Run a SQL sequence reset on all koytola.* apps.

        When a value is manually assigned to an auto-incrementing field
        it doesn't update the field's sequence, which might cause a conflict
        later on.
        """
        commands = StringIO()
        for app in apps.get_app_configs():
            if "project" in app.name:
                call_command(
                    "sqlsequencereset", app.label, stdout=commands, no_color=True
                )
        with connection.cursor() as cursor:
            cursor.execute(commands.getvalue())

    def handle(self, *args, **options):
        # set only our custom plugin to not call external API when preparing
        # example database
        settings.PLUGINS = [
            "koytola.payment.gateways.dummy.plugin.DummyGatewayPlugin",
            "koytola.payment.gateways.dummy_credit_card.plugin."
            "DummyCreditCardGatewayPlugin",
        ]
        self.make_database_faster()
        if options["createsuperuser"]:
            credentials = {"email": "admin@koytola.com", "password": "#admin$"}
            msg = create_superuser(credentials)
            self.stdout.write(msg)
            add_address_to_admin(credentials["email"])
        for msg in create_permission_groups():
            self.stdout.write(msg)
        for msg in create_staffs():
            self.stdout.write(msg)
        for msg in create_hscode_and_product():
            self.stdout.write(msg)
        for msg in create_sheet_companies():
            self.stdout.write(msg)
        for msg in create_product_categories():
            self.stdout.write(msg)
        for msg in create_countries():
            self.stdout.write(msg)
        for msg in create_countries_flag():
            self.stdout.write(msg)
        for msg in create_rosetter():
            self.stdout.write(msg)
        for msg in create_industry():
            self.stdout.write(msg)
        for msg in create_product_certificate():
            self.stdout.write(msg)
        for msg in create_company_certificate():
            self.stdout.write(msg)

