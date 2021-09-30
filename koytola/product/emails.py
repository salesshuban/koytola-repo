from templated_email import send_templated_mail
from ..celeryconf import app
from ..core.emails import get_email_context


@app.task
def send_confirm_order_mail_(template_name, email, order):
    send_kwargs, ctx = get_email_context()
    ctx["order"] = order
    send_templated_mail(
            template_name=template_name,
            recipient_list=[email],
            context=ctx,
            bcc=["export@koytola.com"],
            **send_kwargs,
        )
