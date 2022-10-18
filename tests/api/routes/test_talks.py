"""Place here tests for talks related endpoints"""
from http import HTTPStatus

import pytest
from django.urls import reverse_lazy

from tests.utils.builders.topic import TopicBuilder


@pytest.mark.django_db
def test_get_all_topics_exists(client, reverse_url):
    url = reverse_url("list_topics")
    expected_payload = []

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload


@pytest.mark.django_db
def test_get_all_topics_endpoint_return_topics(client, reverse_url):
    topic = TopicBuilder().with_name("MyTopic").with_description("MyDescription").build()
    url = reverse_url("list_topics")
    expected_payload = [{"id": str(topic.id), "name": "MyTopic"}]

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload


@pytest.mark.django_db
def test_get_topic_endpoint_return_topic(client):
    topic = TopicBuilder().with_name("MyTopic").build()
    url = reverse_lazy("api-alpha:get_topic", kwargs={"topic_id": topic.id})
    expected_payload = {
        "id": str(topic.id),
        "name": "MyTopic",
        "description": "Test Topic Description",
    }

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload
