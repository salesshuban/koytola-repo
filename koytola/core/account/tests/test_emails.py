from unittest import mock

from django.core import mail
from templated_email import get_connection

import koytola.account.emails as account_emails


def test_send_set_password_email(staff_user, site_settings):
    password_set_url = "https://www.example.com"
    template_name = "dashboard/staff/set_password"
    recipient_email = staff_user.email

    account_emails._send_set_password_email(
        recipient_email, password_set_url, template_name
    )

    assert len(mail.outbox) == 1
    sended_message = mail.outbox[0].body
    assert password_set_url in sended_message


@mock.patch("koytola.account.emails.send_templated_mail")
def test_send_email_request_change(
    mocked_templated_email, site_settings, account_user
):
    new_email = "example@example.com"
    template = account_emails.REQUEST_EMAIL_CHANGE_TEMPLATE
    redirect_url = "localhost"
    token = "token_example"
    event_parameters = {"old_email": account_user.email, "new_email": new_email}

    account_emails._send_request_email_change_email(
        new_email, redirect_url, account_user.pk, token, event_parameters
    )
    ctx = {
        "domain": "koytola.com",
        "redirect_url": "localhost?token=token_example",
        "site_name": "koytola.com",
    }
    recipients = [new_email]

    expected_call_kwargs = {
        "context": ctx,
        "from_email": site_settings.default_from_email,
        "template_name": template,
    }

    # mocked_templated_email.assert_called_once()
    mocked_templated_email.assert_called_once_with(
        recipient_list=recipients, **expected_call_kwargs
    )

    # Render the email to ensure there is no error
    email_connection = get_connection()
    email_connection.get_email_message(to=recipients, **expected_call_kwargs)


@mock.patch("koytola.account.emails.send_templated_mail")
def test_send_email_changed_notification(
    mocked_templated_email, site_settings, account_user
):
    old_email = "example@example.com"
    template = account_emails.EMAIL_CHANGED_NOTIFICATION_TEMPLATE
    account_emails.send_user_change_email_notification(old_email)
    ctx = {
        "domain": "koytola.com",
        "site_name": "koytola.com",
    }
    recipients = [old_email]

    expected_call_kwargs = {
        "context": ctx,
        "from_email": site_settings.default_from_email,
        "template_name": template,
    }

    # mocked_templated_email.assert_called_once()
    mocked_templated_email.assert_called_once_with(
        recipient_list=recipients, **expected_call_kwargs
    )

    # Render the email to ensure there is no error
    email_connection = get_connection()
    email_connection.get_email_message(to=recipients, **expected_call_kwargs)
