from unittest.mock import patch

import pytest

from meetupselector.user.tasks import send_registration_mail
from tests.utils.builders import UserBuilder


@pytest.mark.django_db
class TestSendRegistrationEmail:
    @patch("meetupselector.user.tasks.send_templated_email")
    def test_it_sends_an_email_to_new_user_based_in_template(self, send_mail):
        user = (
            UserBuilder()
            .with_email("some@email.xxx")
            .with_password("aaa")
            .build()
        )

        send_registration_mail(user_id=user.id)

        send_mail.assert_called_once_with(
            recipients=[user.email],
            subject="Confirm your registration",
            template="registration_confirmation",
            context={"email_address": user.email},
        )
