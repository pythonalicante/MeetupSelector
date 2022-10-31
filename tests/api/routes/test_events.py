from http import HTTPStatus

import pytest
from django.utils.timezone import now
from freezegun import freeze_time
from hamcrest import (
    assert_that,
    empty,
    equal_to,
    has_entries,
    has_length,
    has_properties,
    is_,
)

from meetupselector.proposals.models import Event
from tests.utils.builders import UserBuilder


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_is_staff_create_event(client, reverse_url):
    url = reverse_url("event")
    name = "eventName"
    description = "description"
    meetup_link = "meetup_link"
    location = "location"
    payload = {
        "name": name,
        "description": description,
        "meetup_link": meetup_link,
        "location": location,
    }
    expected_creation_datetime = now()
    expected_creation_datetime_str = "2022-10-26T23:23:23Z"
    events_before_creation = list(Event.objects.all())
    password = "Password10!"
    staff_user = (
        UserBuilder().with_email("b@b.com").with_password(password).with_is_Staff(True).build()
    )

    client.login(username=staff_user.email, password=password)

    response = client.post(url, data=payload, content_type="application/json")

    events_after_creation = Event.objects.all()
    assert_that(response.status_code, equal_to(HTTPStatus.CREATED))
    assert_that(events_before_creation, is_(empty()))
    assert_that(events_after_creation, has_length(1))
    created_event = events_after_creation.first()
    assert_that(
        response.json(),
        has_entries(
            {
                "id": str(created_event.pk),
                "created_at": expected_creation_datetime_str,
                "updated_at": expected_creation_datetime_str,
                "name": name,
                "description": description,
                "meetup_link": meetup_link,
                "location": location,
            }
        ),
    )
    assert_that(
        created_event,
        has_properties(
            id=created_event.pk,
            created_at=expected_creation_datetime,
            updated_at=expected_creation_datetime,
            name=name,
            description=description,
            location=location,
            meetup_link=meetup_link,
            done=False,
        ),
    )


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_is_not_staff_create_event(client, reverse_url):
    url = reverse_url("event")
    name = "eventName"
    description = "description"
    meetup_link = "meetup_link"
    location = "location"
    payload = {
        "name": name,
        "description": description,
        "meetup_link": meetup_link,
        "location": location,
    }
    events_before_creation = list(Event.objects.all())
    password = "Password10!"
    staff_user = (
        UserBuilder().with_email("b@b.com").with_password(password).with_is_Staff(False).build()
    )

    client.login(username=staff_user.email, password=password)

    response = client.post(url, data=payload, content_type="application/json")

    events_after_creation = Event.objects.all()
    assert_that(response.status_code, equal_to(HTTPStatus.UNAUTHORIZED))
    assert_that(events_before_creation, is_(empty()))
    assert_that(events_after_creation, has_length(0))
