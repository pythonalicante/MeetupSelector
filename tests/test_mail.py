import os
from unittest.mock import patch

from django.test import override_settings
from hamcrest import assert_that, equal_to

from meetupselector.mail import _render_template, send_templated_email

current_folder = os.path.abspath(os.path.dirname(__file__))
templates_settings = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f"{current_folder}/templates"],
        "APP_DIRS": False,
    },
]
valid_context = {"name": "Facundo"}


class TestSendTemplatedEmail:
    @override_settings(TEMPLATES=templates_settings)
    def test_it_renders_template_with_context(self):
        expected_txt = "Hi Facundo!\n"
        template_name = "any_template.txt"

        rendered_content = _render_template(template_name, valid_context)

        assert_that(rendered_content, equal_to(expected_txt))

    @override_settings(TEMPLATES=templates_settings, DEFAULT_FROM_EMAIL="a@b.com")
    @patch("meetupselector.mail.send_mail")
    def test_it_sends_email(self, django_send_mail):
        recipients = ["no_hay_nada@parasiempre.com", "la_chispa_adecuada@hds.es"]
        subject = "Sad but true"
        expected_txt = "Hi Facundo!\n"
        expected_html = "<!DOCTYPE html><body>Hi Facundo</body></html>\n"

        send_templated_email(
            recipients=recipients,
            subject=subject,
            template_name="any_template",
            context=valid_context,
        )

        django_send_mail.assert_called_once_with(
            subject=subject,
            message=expected_txt,
            from_email="a@b.com",
            recipient_list=recipients,
            fail_silently=False,
            html_message=expected_html,
        )
