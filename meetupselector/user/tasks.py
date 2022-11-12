from uuid import UUID

from celery import shared_task
from django.utils.translation import gettext_lazy as _

from meetupselector.mail import send_templated_email
from meetupselector.user.models import User


@shared_task(bind=True)
def send_registration_mail(self, user_id: UUID):
    user = User.objects.get(id=user_id)

    send_templated_email(
        recipients=[user.email],
        subject=_("Confirm your registration"),
        template="registration_confirmation",
        context={"email_address": user.email},
    )
