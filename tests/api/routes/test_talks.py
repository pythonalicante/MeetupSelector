"""Place here tests for talks related endpoints"""
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse_lazy

from meetupselector.talks.models import Talk
from tests.utils.builders.talk import TalkBuilder
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


@pytest.mark.django_db
def test_get_all_talks_exists(client, reverse_url):
    url = reverse_url("list_talks")
    expected_payload = []

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload


@pytest.mark.django_db
def test_get_all_talks_endpoint_return_talks(client, reverse_url):
    talk = (
        TalkBuilder()
        .with_name("MyTalk")
        .with_description("MyDescription")
        .with_headline("My headline")
        .with_type("T")
        .with_difficulty("E")
        .with_duration("00:00:12")
        .build()
    )
    url = reverse_url("list_talks")
    expected_payload = [{"id": str(talk.id), "name": "MyTalk", "headline": "My headline"}]

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload


@pytest.mark.django_db
def test_get_talk_endpoint_return_talk(client):
    topic = TopicBuilder().with_name("MyTopic").build()
    talk = (
        TalkBuilder()
        .with_name("MyTalk")
        .with_description("MyDescription")
        .with_headline("My headline")
        .with_type("T")
        .with_difficulty("E")
        .with_duration("500 00:00:12")
        .with_topic(topic)
        .build()
    )
    url = reverse_lazy("api-alpha:get_talk", kwargs={"talk_id": talk.id})
    expected_payload = {
        "id": str(talk.id),
        "name": "MyTalk",
        "description": "MyDescription",
        "headline": "My headline",
        "type": "T",
        "difficulty": "E",
        "duration": "P500DT00H00M12S",
        "topics": [{"id": str(topic.id), "name": topic.name, "description": topic.description}],
    }

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_payload


@pytest.mark.django_db
def test_post_talk_endpoint_can_create_talk(client: Client, reverse_url):
    url = reverse_url("list_talks")  # Is the same endpoint
    topic = TopicBuilder().with_name("MyTopic").build()
    talk_data = {
        "name": "MyTalk",
        "description": "MyDescription",
        "headline": "My headline",
        "type": "T",
        "difficulty": "E",
        "duration": 500,
        "topics": [str(topic.id)],
    }

    response = client.post(url, data=talk_data, content_type="application/json")

    assert response.status_code == HTTPStatus.CREATED
    assert len(Talk.objects.all()) == 1


@pytest.mark.django_db
def test_patch_talk_endpoint_can_update_talk(client: Client, reverse_url):
    url = reverse_url("list_talks")  # Is the same endpoint
    topic = TopicBuilder().with_name("MyTopic").build()
    talk = (
        TalkBuilder()
        .with_name("MyTalk")
        .with_description("MyDescription")
        .with_headline("My headline")
        .with_type("T")
        .with_difficulty("E")
        .with_duration("500 00:00:12")
        .with_topic(topic)
        .build()
    )
    new_description_expected = "My New Description"
    talk_new_data = {
        "id": str(talk.id),
        "description": new_description_expected,
    }

    response = client.patch(url, data=talk_new_data, content_type="application/json")

    assert response.status_code == HTTPStatus.OK
    talk.refresh_from_db()
    assert talk.description == new_description_expected
