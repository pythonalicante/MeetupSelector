from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib.auth import authenticate
from hamcrest import (
    assert_that,
    contains_string,
    empty,
    equal_to,
    has_length,
    is_,
    is_not,
    none,
)

from meetupselector.user.models import User
from tests.utils.builders import UserBuilder


@pytest.mark.django_db
class TestUserLogin:
    def test_succesful_login(self, client, reverse_url):
        email = "registered@user.com"
        password = "aaa"
        UserBuilder().with_email(email).with_password(password).build()

        assert_that(client.cookies, empty())
        url = reverse_url("login")
        response = client.post(
            url, data={"email": email, "password": password}, content_type="application/json"
        )

        assert_that(client.cookies, is_not(empty()))
        assert_that(response.status_code, equal_to(HTTPStatus.OK))

    def test_bad_credentials_login(self, client, reverse_url):
        email = "registered@user.com"
        password = "aaa"
        UserBuilder().with_email(email).with_password(password).build()

        bad_password = "bbb"
        assert_that(password, is_not(equal_to(bad_password)))

        assert_that(client.cookies, empty())
        url = reverse_url("login")
        response = client.post(
            url, data={"email": email, "password": bad_password}, content_type="application/json"
        )

        assert_that(client.cookies, empty())
        assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))

    def test_inexistent_user_login(self, client, reverse_url):
        email = "nonregistered@user.com"
        password = "aaa"

        assert_that(client.cookies, empty())
        url = reverse_url("login")
        response = client.post(
            url, data={"email": email, "password": password}, content_type="application/json"
        )

        assert_that(client.cookies, empty())
        assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))


@pytest.mark.django_db
class TestUserSignIn:

    password_error_msg = (
        "password requirements: min. length of 8 chars, "
        "one uppercase char, one lowercase char, one digit, "
        "one special char (not letter, not number)"
    )

    @pytest.mark.parametrize(
        "email,password,expected_error",
        [
            ("wrong_email", "Valid_P4ssw@rd", "not a valid email address"),
            ("a@b.com", "Sh@rt1", password_error_msg),
            ("a@b.com", "ABC123@ZZ", password_error_msg),
            ("a@b.com", "abc123@zz", password_error_msg),
            ("a@b.com", "abcABC@zz", password_error_msg),
            ("a@b.com", "abcABC1zz", password_error_msg),
        ],
        ids=[
            "wrong_email",
            "short_password",
            "not_lowercase_letter_password",
            "not_uppercase_letter_password",
            "not_digit_password",
            "not_special_char_password",
        ],
    )
    def test_create_user_validates_payload(
        self, client, reverse_url, email, password, expected_error
    ):
        url = reverse_url("create_user")
        payload = {
            "email": email,
            "password": password,
        }

        response = client.post(url, data=payload, content_type="application/json")

        users_after_creation = User.objects.all()
        assert_that(response.status_code, equal_to(HTTPStatus.UNPROCESSABLE_ENTITY))
        assert_that(str(response.json()), contains_string(expected_error))
        assert_that(users_after_creation, is_(empty()))

    @patch("meetupselector.user.services.user.send_registration_mail")
    def test_create_user_with_valid_payload(self, mail_task, client, reverse_url):
        email = "luke@starwars.com"
        password = "Any_Valid_P4ssw@rd"
        url = reverse_url("create_user")
        payload = {
            "email": email,
            "password": password,
        }
        users_before_creation = list(User.objects.all())

        response = client.post(url, data=payload, content_type="application/json")

        users_after_creation = User.objects.all()
        assert_that(response.status_code, equal_to(HTTPStatus.CREATED))
        assert_that(users_before_creation, is_(empty()))
        assert_that(users_after_creation, has_length(1))
        created_user = users_after_creation.first()
        assert_that(created_user.email, equal_to(email))
        assert_that(created_user.is_active, is_(False))
        assert_that(authenticate(username=email, password=password), is_(none()))
        mail_task.delay.assert_called_once_with(user_id=created_user.id)
