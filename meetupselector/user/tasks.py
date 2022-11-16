from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext_lazy

from meetupselector.mail import send_templated_email


@shared_task(bind=True)
def send_registration_mail(_, email: str, confirmation_url: str):
    context = {
        "project_name": settings.PROJECT_NAME,
        "confirmation_url": confirmation_url,
    }
    send_templated_email(
        recipients=[email],
        subject=gettext_lazy("Confirm your registration"),  # type: ignore
        template_name="registration_confirmation",
        context=context,
    )
