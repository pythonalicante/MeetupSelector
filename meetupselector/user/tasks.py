from uuid import UUID

from celery import shared_task


@shared_task(bind=True)
def send_registration_mail(self, user_id: UUID):
    print(f"User: {user_id}")
