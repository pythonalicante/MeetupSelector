from http import HTTPStatus

import pytest
from hamcrest import assert_that, empty, equal_to, is_not

from tests.utils.builders import UserBuilder


@pytest.mark.django_db
def test_succesful_login(client, reverse_url):
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


@pytest.mark.django_db
def test_bad_credentials_login(client, reverse_url):
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


@pytest.mark.django_db
def test_inexistent_user_login(client, reverse_url):
    email = "nonregistered@user.com"
    password = "aaa"

    assert_that(client.cookies, empty())
    url = reverse_url("login")
    response = client.post(
        url, data={"email": email, "password": password}, content_type="application/json"
    )

    assert_that(client.cookies, empty())
    assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
