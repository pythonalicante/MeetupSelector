from datetime import timedelta
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
    only_contains,
)

from meetupselector.proposals.models import Event
from tests.utils.builders import EventBuilder, UserBuilder


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_is_staff_create_event(client, reverse_url):
    url = reverse_url("create_list_event")
    name = "eventName"
    description = "description"
    meetup_link = "https://www.meetup.com/"
    location = "location"
    date = (now() + timedelta(days=5)).date()
    start_time = now().time()
    duration = timedelta(hours=2)
    payload = {
        "name": name,
        "description": description,
        "meetup_link": meetup_link,
        "location": location,
        "date": str(date),
        "start_time": str(start_time),
        "duration": duration.seconds,
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
                "date": str(date),
                "start_time": str(start_time),
                "duration": duration.seconds,
            }
        ),
    )
    # breakpoint()
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
            date=date,
            start_time=start_time,
            duration=duration,
        ),
    )


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_is_not_staff_create_event(client, reverse_url):
    url = reverse_url("create_list_event")
    name = "eventName"
    description = "description"
    meetup_link = "https://www.meetup.com/"
    location = "location"
    date = str((now() + timedelta(days=5)).date())
    start_time = str(now().time())
    duration = timedelta(hours=2)
    payload = {
        "name": name,
        "description": description,
        "meetup_link": meetup_link,
        "location": location,
        "date": date,
        "start_time": start_time,
        "duration": duration.seconds,
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


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_list_events_endpoint_return_events(client, reverse_url):
    event1 = (
        EventBuilder()
        .with_name("event1")
        .with_description("first event description")
        .with_meetup_link("https://www.meetup.com/event1")
        .with_location("first event location")
        .with_date(now() + timedelta(days=5))
        .with_start_time(now().time())
        .with_duration(timedelta(hours=2))
        .build()
    )
    event2 = (
        EventBuilder()
        .with_name("event2")
        .with_description("second event description")
        .with_meetup_link("https://www.meetup.com/event2")
        .with_location("second event location")
        .with_date(now() + timedelta(days=5))
        .with_start_time(now().time())
        .with_duration(timedelta(hours=2))
        .build()
    )
    expected_creation_datetime_str = "2022-10-26T23:23:23Z"
    expected_payload = [
        {
            "id": str(event1.id),
            "created_at": expected_creation_datetime_str,
            "updated_at": expected_creation_datetime_str,
            "name": event1.name,
            "description": event1.description,
            "meetup_link": event1.meetup_link,
            "location": event1.location,
            "date": "2022-10-31",
            "start_time": "23:23:23",
            "duration": event1.duration_seconds,
        },
        {
            "id": str(event2.id),
            "created_at": expected_creation_datetime_str,
            "updated_at": expected_creation_datetime_str,
            "name": event2.name,
            "description": event2.description,
            "meetup_link": event2.meetup_link,
            "location": event2.location,
            "date": "2022-10-31",
            "start_time": "23:23:23",
            "duration": event2.duration_seconds,
        },
    ]
    url = reverse_url("create_list_event")

    response = client.get(url)
    listed_events = response.json()

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(listed_events, has_length(2))
    assert_that(
        listed_events,
        only_contains(
            has_entries(**expected_payload[0]),
            has_entries(**expected_payload[1]),
        ),
    )
