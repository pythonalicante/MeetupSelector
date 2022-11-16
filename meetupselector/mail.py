from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Engine


def send_templated_email(
    recipients: list[str],
    subject: str,
    template_name: str,
    context: dict[str, Any],
):
    """IMPORTANT: wrap this function call within any async procedure.
    In example: a @shared_task decorated funtion.

    Sends an email to all recipients, with a rendered template.
    Template must exist in both versions: TXT and HTML.
    """
    send_mail(
        subject=subject,
        message=_render_template(f"{template_name}.txt", context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
        html_message=_render_template(f"{template_name}.html", context),
    )


def _render_template(template_file_name: str, context: dict[str, Any]) -> str:
    engine = Engine.get_default()
    return engine.get_template(template_file_name).render(Context(context))
