from django.db import models

from ..account.models import User
from ..core.permissions import HelpdeskPermissions


TICKET_TYPE = [
    ("Support", "Support"),
    ("Feedback", "Feedback"),
    ("Recommendation", "Recommendation"),
    ("New Feature Request", "New Feature Request"),
    ("Other", "Other")
]
TICKET_STATUS = [
    ("New", "New"),
    ("On Progress", "On Progress"),
    ("Completed", "Completed"),
    ("Other", "Other")
]


class HelpdeskQuerySet(models.QuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(HelpdeskPermissions.MANAGE_TICKETS)

    def visible_to_user(self, user):
        if self.user_has_access_to_all(user):
            return self.all()
        return self.filter(user=user)


class MessageQuerySet(models.QuerySet):
    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active and user.has_perm(HelpdeskPermissions.MANAGE_TICKETS)

    def visible_to_user(self, user):
        if self.user_has_access_to_all(user):
            return self.all()
        return self.filter(ticket__user=user)


class Ticket(models.Model):
    # Ticket Information
    user = models.ForeignKey(
        User,
        related_name="tickets",
        on_delete=models.SET_NULL,
        null=True
    )
    type = models.TextField(choices=TICKET_TYPE, default="Support")
    subject = models.CharField(max_length=128, default="", blank=False)
    content = models.TextField(max_length=600, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    # Ticket Management
    notes = models.CharField(max_length=256, blank=True, default="")
    status = models.TextField(choices=TICKET_STATUS, default="New")
    update_date = models.DateTimeField(auto_now=True)

    objects = HelpdeskQuerySet.as_manager()

    class Meta:
        verbose_name = "Helpdesk Ticket"
        verbose_name_plural = "Helpdesk Tickets"
        ordering = ["-creation_date"]

    def __str__(self):
        return "Ticket #" + str(self.id) + " - User: " + self.user.user_id


class Message(models.Model):
    """ Model representing a Helpdesk Ticket messages. """
    ticket = models.ForeignKey(
        Ticket,
        related_name="messages",
        on_delete=models.SET_NULL,
        null=True
    )
    content = models.TextField(max_length=600, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = "Ticket Message"
        verbose_name_plural = "Ticket Messages"
        ordering = ["-creation_date"]

    def __str__(self):
        return "Ticket #" + str(self.ticket_id) + " - Message: " + str(self.id)
