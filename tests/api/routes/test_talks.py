from http import HTTPStatus

import pytest
from django.urls import reverse_lazy
from freezegun import freeze_time
from hamcrest import assert_that, empty, equal_to, has_entries, has_item

from tests.utils.builders import TopicBuilder


@pytest.mark.django_db
def test_get_all_topics_exists(client, reverse_url):
    url = reverse_url("list_topics")

    response = client.get(url)

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(response.json(), empty())


@pytest.mark.django_db
def test_get_all_topics_endpoint_return_topics(client, reverse_url):
    name = "My Topic"
    description = "Test Topic Description"
    topic = TopicBuilder().with_name(name).with_description(description).build()
    url = reverse_url("list_topics")

    response = client.get(url)

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(
        response.json(), has_item({"id": str(topic.id), "name": name, "description": description})
    )


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_get_topic_endpoint_return_topic(client):
    name = "MyTopic"
    description = "Test Topic Description"
    topic = TopicBuilder().with_name(name).with_description(description).build()
    url = reverse_lazy("api-alpha:get_topic", kwargs={"topic_id": topic.id})
    expected_creation_datetime_str = "2022-10-26T23:23:23Z"

    response = client.get(url)

    assert_that(response.status_code, equal_to(HTTPStatus.OK))
    assert_that(
        response.json(),
        has_entries(
            {
                "id": str(topic.id),
                "name": name,
                "description": description,
                "created_at": expected_creation_datetime_str,
                "updated_at": expected_creation_datetime_str,
            }
        ),
    )
