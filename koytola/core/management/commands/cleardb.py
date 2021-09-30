"""Clear the database preserving site's configuration.

This command clears the database from data such as orders, profiles or
accounts. It doesn't remove site's configuration, such as: staff accounts,
plugin configurations, site settings or navigation menus.
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from ....account.models import User
from ....analytics.models import Tracking
from ....helpdesk.models import Ticket, Message
from ....news.models import News
from ....order.models import Order
from ....page.models import Page, PageType
from ....payment.models import Payment, Transaction
from ....product.models import (
    Category,
    Product,
    ProductVideo,
    ProductPrice,
    ProductImage
)
from ....profile.models import (
    Company,
    Certificate,
    Brochure,
    Video,
    SocialResponsibility,
)
from ....site.models import ContactMessage, SiteSubscriber
from ....webhook.models import Webhook


class Command(BaseCommand):
    help = "Removes data from the database preserving site configuration."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete-staff",
            action="store_true",
            help="Delete staff user accounts (doesn't delete superuser accounts).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allows running the cleardb command in DEBUG=False mode.",
        )

    def handle(self, **options):
        force = options.get("force", False)
        if not settings.DEBUG and not force:
            raise CommandError("Cannot clear the database in DEBUG=False mode.")

        # Analytics Module
        Tracking.objects.all().delete()
        self.stdout.write("Removed analytics tracking")

        # Helpdesk Module
        Ticket.objects.all().delete()
        self.stdout.write("Removed helpdesk ticket messages")

        Message.objects.all().delete()
        self.stdout.write("Removed helpdesk tickets")

        # News Module
        News.objects.all().delete()
        self.stdout.write("Removed news")

        # Payment module
        Transaction.objects.all().delete()
        self.stdout.write("Removed transactions")

        Payment.objects.all().delete()
        self.stdout.write("Removed payments")

        # Order Module
        Order.objects.all().delete()
        self.stdout.write("Removed orders")

        # Page Module
        Page.objects.all().delete()
        self.stdout.write("Removed pages")

        PageType.objects.all().delete()
        self.stdout.write("Removed page types")

        # Product Module
        Category.objects.all().delete()
        self.stdout.write("Removed platform categories")

        Product.objects.all().delete()
        self.stdout.write("Removed products")

        ProductImage.objects.all().delete()
        self.stdout.write("Removed product images")

        ProductPrice.objects.all().delete()
        self.stdout.write("Removed product prices")

        ProductVideo.objects.all().delete()
        self.stdout.write("Removed product videos")

        # Profile Module
        Company.objects.all().delete()
        self.stdout.write("Removed profile companies")

        Brochure.objects.all().delete()
        self.stdout.write("Removed company brochures")

        Certificate.objects.all().delete()
        self.stdout.write("Removed company certificates")

        SocialResponsibility.objects.all().delete()
        self.stdout.write("Removed company social responsibilities")

        Video.objects.all().delete()
        self.stdout.write("Removed company videos")

        # Site Module
        ContactMessage.objects.all().delete()
        self.stdout.write("Removed site contact messages")

        SiteSubscriber.objects.all().delete()
        self.stdout.write("Removed site subscribers")

        # Webhook Module
        Webhook.objects.all().delete()
        self.stdout.write("Removed webhooks")

        # Delete all users except for staff members.
        staff = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        User.objects.exclude(pk__in=staff).delete()
        self.stdout.write("Removed accounts")

        should_delete_staff = options.get("delete_staff")
        if should_delete_staff:
            staff = staff.exclude(is_superuser=True)
            staff.delete()
            self.stdout.write("Removed staff users")

        # Remove addresses of staff members. Used to clear saved addresses of staff
        # accounts used on demo for testing checkout.
        for user in staff:
            user.addresses.all().delete()
        self.stdout.write("Removed staff addresses")
