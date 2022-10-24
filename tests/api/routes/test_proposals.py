from http import HTTPStatus

import pytest

from tests.utils.builders import (
    ProposalBuilder,
    TalkBuilder,
    TopicBuilder,
)


@pytest.mark.django_db
def test_create_proposal(client, reverse_url):
    url = reverse_url("create_list_proposal")
    subject = "anything"
    description = "Any description"
    difficulty = "E"
    lang = "ES_ES"
    topic = TopicBuilder().build()
    talk = TalkBuilder().build()
    payload = {
        "subject": subject,
        "description": description,
        "difficulty": difficulty,
        "language": lang,
        "topics": [topic.id],
        "talks": [talk.id],
        "proposed_by": ,
        "liked_by": ,
        "done": False,
    }

    response = client.post(url, data=payload, content_type="application/json")

    breakpoint()

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_payload
