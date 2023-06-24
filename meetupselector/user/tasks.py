from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy

from meetupselector.mail import send_templated_email
from meetupselector.user.token import token_generator

User = get_user_model()


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


@shared_task(bind=True)
def send_reset_password_email(_, user_id: str):
    subject = str(gettext_lazy("Password Reset Instructions"))
    domain_name = settings.SITE_DOMAIN
    app_name = settings.PROJECT_NAME
    user = User.objects.get(pk=user_id)
    reset_password_link = (
        f"http://{domain_name}/api/users/reset_password/"
        f"{urlsafe_base64_encode(force_bytes(user.pk))}/{token_generator.make_token(user)}"
    )
    context = {
        "user": user.email,
        "reset_password_link": reset_password_link,
        "app_name": app_name,
    }

    send_templated_email(
        recipients=[user.email],
        subject=subject,
        template_name="password_reset",
        context=context,
    )
