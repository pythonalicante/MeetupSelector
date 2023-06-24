from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from hamcrest import (
    assert_that,
    contains_string,
    empty,
    equal_to,
    has_entry,
    has_key,
    has_length,
    is_,
    is_not,
    none,
    not_,
)

from meetupselector.user.models import User
from meetupselector.user.token import token_generator
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

    @pytest.mark.parametrize(
        "GDPR_accepted",
        [
            (True),
            (False),
        ],
        ids=[
            "GDPR_accepted is True",
            "GDPR_accepted is False",
        ],
    )
    def test_create_user_with_GDPR_accepted(self, client, reverse_url, GDPR_accepted):
        url = reverse_url("create_user")
        payload = {
            "email": "luke@starwars.com",
            "password": "Any_Valid_P4ssw@rd",
            "GDPR_accepted": GDPR_accepted,
        }
        response = client.post(url, data=payload, content_type="application/json")

        users_after_creation = User.objects.all()
        assert_that(users_after_creation.first().GDPR_accepted, equal_to(GDPR_accepted))
        assert_that(users_after_creation.first().email, equal_to("luke@starwars.com"))
        assert_that(response.status_code, equal_to(HTTPStatus.CREATED))
        assert_that(users_after_creation, has_length(1))

    @patch("meetupselector.user.services.user.send_registration_mail")
    def test_create_user_with_valid_payload(self, send_registration_mail_task, client, reverse_url):
        email = "luke@starwars.com"
        password = "Any_Valid_P4ssw@rd"
        GDPR_accepted: bool = True
        url = reverse_url("create_user")
        payload = {
            "email": email,
            "password": password,
            "GDPR_accepted": GDPR_accepted,
        }
        users_before_creation = list(User.objects.all())

        response = client.post(url, data=payload, content_type="application/json")

        users_after_creation = User.objects.all()
        assert_that(response.status_code, equal_to(HTTPStatus.CREATED))
        assert_that(users_before_creation, is_(empty()))
        assert_that(users_after_creation, has_length(1))
        created_user = users_after_creation.first()
        confirmation_url_path = reverse_url(
            settings.CONFIRMATION_URL_NAME, {"user_id": str(created_user.id)}
        )
        confirmation_url = f"http://testserver{confirmation_url_path}"
        assert_that(created_user.email, equal_to(email))
        assert_that(created_user.GDPR_accepted, equal_to(GDPR_accepted))
        assert_that(created_user.is_active, is_(False))
        assert_that(authenticate(username=email, password=password), is_(none()))
        send_registration_mail_task.delay.assert_called_once_with(
            email=created_user.email,
            confirmation_url=f"{confirmation_url}/{str(created_user.id)}",
        )

    def test_user_account_confirmation(self, client, reverse_url):
        user = UserBuilder().with_is_active(False).build()
        url = f"http://testserver/api/users/signin_confirmation/{str(user.id)}"

        response = client.get(url)

        assert_that(user.is_active, is_(False))
        user.refresh_from_db()
        assert_that(user.is_active, is_(True))
        assert_that(response.headers, has_entry("Location", "http://testserver/"))
        assert_that(response.status_code, equal_to(HTTPStatus.FOUND))

    def test_user_account_confirmation_user_not_found(self, client, reverse_url):
        user = UserBuilder().with_is_active(False).build()
        url = "http://testserver/api/users/signin_confirmation/wrong_uid"

        response = client.get(url)

        user.refresh_from_db()
        assert_that(user.is_active, is_(False))
        assert_that(response.headers, not_(has_key("Location")))
        assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))


@pytest.mark.django_db
class TestUserDelete:
    def test_logged_in_user_can_delete_own_account(self, client, reverse_url):
        email_account_owner = "user1_registered@user.com"
        password_account_owner = "Password10!"
        (
            UserBuilder()
            .with_email(email_account_owner)
            .with_password(password_account_owner)
            .build()
        )

        url = reverse_url("/")
        client.login(email=email_account_owner, password=password_account_owner)
        response = client.delete(url, content_type="application/json")
        created_users_after_delete = User.objects.all()

        assert_that(response.status_code, equal_to(HTTPStatus.OK))
        assert_that(created_users_after_delete, is_(empty()))

    def test_not_logged_in_user_cannot_delete__account(self, client, reverse_url):
        email_user = "user1_registered@user.com"
        password_user = "Password10!"
        UserBuilder().with_email(email_user).with_password(password_user).build()
        url = reverse_url("/")
        response = client.delete(url, content_type="application/json")
        created_users_after_delete = User.objects.all()

        assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
        assert_that(created_users_after_delete, has_length(1))


@pytest.mark.django_db
class TestResetUserPassword:
    def test_send_email_to_reset_password_for_registered_account(
        self,
        client,
        reverse_url,
    ):
        email = "user1_registered@user.com"
        old_password = "Password10!"
        user = (
            UserBuilder().with_email(email).with_password(old_password).with_is_active(True).build()
        )
        payload = {
            "email": user.email,
        }
        url = reverse_url("reset_password_link")
        response = client.post(url, data=payload, content_type="application/json")

        assert_that(response.status_code, equal_to(HTTPStatus.OK))

    def test_send_email_to_reset_password_with_unregistered_email_address(
        self,
        reverse_url,
        client,
    ):
        email = "user1_registered@user.com"
        payload = {
            "email": email,
        }
        url = reverse_url("reset_password_link")
        response = client.post(url, data=payload, content_type="application/json")

        assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

    def test_generated_url_returns_password_reset_url(
        self,
        reverse_url,
        client,
    ):
        email = "user1_registered@user.com"
        old_password = "Password10!"
        new_password = "New_Password10!"
        user = (
            UserBuilder().with_email(email).with_password(old_password).with_is_active(True).build()
        )

        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        payload = {
            "new_password": new_password,
        }

        url = reverse_url(
            "reset_password",
            kwargs={"uidb64": uid, "token": token},
        )
        response = client.post(url, data=payload, content_type="application/json")

        user_with_new_password = authenticate(email=email, password=new_password)
        user_with_old_password = authenticate(email=email, password=old_password)

        assert_that(response.status_code, equal_to(HTTPStatus.OK))
        assert_that(user_with_new_password is not None)
        assert_that(user_with_new_password.id, equal_to(user.pk))
        assert_that(user_with_old_password is None)

    def test_bad_url_fails_to_reset_password_reset_url(
        self,
        reverse_url,
        client,
    ):
        email = "user1_registered@user.com"
        old_password = "Password10!"
        new_password = "New_Password10!"
        user = (
            UserBuilder().with_email(email).with_password(old_password).with_is_active(True).build()
        )

        user_2_email = "user2_registered@user.com"
        user_2_password = "password10!"
        user_2 = (
            UserBuilder()
            .with_email(user_2_email)
            .with_password(user_2_password)
            .with_is_active(True)
            .build()
        )

        token = token_generator.make_token(user_2)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        payload = {
            "new_password": new_password,
        }

        url = reverse_url(
            "reset_password",
            kwargs={"uidb64": uid, "token": token},
        )
        response = client.post(url, data=payload, content_type="application/json")

        user_with_old_password = authenticate(email=email, password=old_password)
        user_with_new_password = authenticate(email=email, password=new_password)

        user_2_with_old_password = authenticate(email=user_2_email, password=user_2_password)
        user_2_with_new_password = authenticate(email=user_2_email, password=new_password)

        assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND))

        assert_that(user_with_new_password is None)
        assert_that(user_with_old_password is not None)
        assert_that(user_2_with_old_password is not None)
        assert_that(user_2_with_new_password is None)
