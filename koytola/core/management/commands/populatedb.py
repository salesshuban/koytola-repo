from io import StringIO

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from ....account.utils import create_superuser
from ...utils.random_data import (
    add_address_to_admin,
    create_account_events,
    create_menus,
    create_news,
    create_pages,
    create_page_types,
    create_permission_groups,
    create_companies,
    create_staffs,
    create_tracking,
    create_users,
    create_users_and_companies,
    create_sheet_companies
)


class Command(BaseCommand):
    help = "Populate database with test objects"
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
        parser.add_argument(
            "--skipsequencereset",
            action="store_true",
            dest="skipsequencereset",
            default=False,
            help="Don't reset SQL sequences that are out of sync.",
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
            print(commands.getvalue())
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
        create_images = not options["withoutimages"]
        for msg in create_page_types():
            self.stdout.write(msg)
        for msg in create_pages():
            self.stdout.write(msg)
        for msg in create_menus():
            self.stdout.write(msg)
        for msg in create_news():
            self.stdout.write(msg)

        for msg in create_users(10):
            self.stdout.write(msg)
        for msg in create_companies(10):
            self.stdout.write(msg)
        for msg in create_users_and_companies(30):
            self.stdout.write(msg)
        for msg in create_account_events(10):
            self.stdout.write(msg)

        for msg in create_tracking(500):
            self.stdout.write(msg)

        if options["createsuperuser"]:
            credentials = {"email": "admin@koytola.com", "password": "admin"}
            msg = create_superuser(credentials)
            self.stdout.write(msg)
            add_address_to_admin(credentials["email"])
        if not options["skipsequencereset"]:
            self.sequence_reset()

        for msg in create_permission_groups():
            self.stdout.write(msg)
        for msg in create_staffs():
            self.stdout.write(msg)
