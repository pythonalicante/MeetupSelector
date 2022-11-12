from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template import Engine, Context


def send_templated_email(
    recipients: list[str],
    subject: str,
    template: str,
    context: dict[Any]
):
    """ IMPORTANT: wrap this function call with any async procedure. In example, a @shared_task decorated funtion.

    Send an email to all recipients, with a rendered template.
    Template must exist in both versions: TXT and HTML.
    """
    send_mail(
        subject=subject,
        message=_render_template(f'{template}.txt', context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
        html_message=_render_template(f'{template}.html', context)
    )


def _render_template(template, context):
    engine = Engine.get_default()
    return engine.get_template(template).render(Context(context))
