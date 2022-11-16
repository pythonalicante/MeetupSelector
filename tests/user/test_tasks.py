from unittest.mock import patch

import pytest
from django.conf import settings
from django.test import override_settings

from meetupselector.user.tasks import send_registration_mail
from tests.utils.builders import UserBuilder


@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
@pytest.mark.django_db
class TestSendRegistrationEmail:
    @override_settings(PROJECT_NAME="my_fancy_project")
    @patch("meetupselector.user.tasks.send_templated_email")
    def test_it_sends_an_email_to_new_user_based_in_template(
        self, send_templated_email, reverse_url
    ):
        user = UserBuilder().with_email("some@email.xxx").with_password("aaa").build()
        confirmation_url = reverse_url(settings.CONFIRMATION_URL_NAME)
        expected_context = {
            "project_name": "my_fancy_project",
            "confirmation_url": confirmation_url,
        }

        task_handle = send_registration_mail.delay(user.email, confirmation_url)
        task_handle.get()

        send_templated_email.assert_called_once_with(
            recipients=[user.email],
            subject="Confirm your registration",
            template_name="registration_confirmation",
            context=expected_context,
        )
