import uuid
from http import HTTPStatus
from re import sub

import pytest
from django.urls import reverse_lazy
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

from meetupselector.proposals.models import Proposal
from tests.utils.builders import ProposalBuilder, TopicBuilder, UserBuilder


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_create_proposal(client, reverse_url):
    url = reverse_url("create_list_proposal")
    subject = "anything"
    description = "Any description"
    difficulty = "E"
    lang = "ES_ES"
    proposer = UserBuilder().with_email("a@a.com").build()
    fanboy = UserBuilder().with_email("b@b.com").build()
    topic = TopicBuilder().build()
    payload = {
        "subject": subject,
        "description": description,
        "difficulty": difficulty,
        "language": lang,
        "topics": [topic.id],
        "proposed_by": str(proposer.pk),
        "liked_by": [str(fanboy.pk)],
        "done": False,
    }
    expected_creation_datetime = now()
    expected_creation_datetime_str = "2022-10-26T23:23:23Z"
    proposals_before_creation = list(Proposal.objects.all())

    response = client.post(url, data=payload, content_type="application/json")

    proposals_after_creation = Proposal.objects.all()
    assert_that(response.status_code, equal_to(HTTPStatus.CREATED))
    assert_that(proposals_before_creation, is_(empty()))
    assert_that(proposals_after_creation, has_length(1))
    created_proposal = proposals_after_creation.first()
    assert_that(
        response.json(),
        has_entries(
            {
                "id": str(created_proposal.pk),
                "created_at": expected_creation_datetime_str,
                "updated_at": expected_creation_datetime_str,
                "subject": subject,
                "description": description,
                "difficulty": difficulty,
                "language": lang,
                "topics": [
                    {
                        "id": str(topic.id),
                        "name": topic.name,
                        "description": topic.description,
                        "created_at": expected_creation_datetime_str,
                        "updated_at": expected_creation_datetime_str,
                    }
                ],
                "proposed_by": str(proposer.id),
                "liked_by": [str(fanboy.id)],
                "done": False,
            }
        ),
    )
    assert_that(
        created_proposal,
        has_properties(
            id=created_proposal.pk,
            created_at=expected_creation_datetime,
            updated_at=expected_creation_datetime,
            subject=subject,
            description=description,
            difficulty=difficulty,
            language=lang,
            proposed_by=proposer,
            done=False,
        ),
    )
    topics = created_proposal.topics.all()
    assert_that(topics, has_length(1))
    assert_that(topics.first().id, equal_to(topic.id))
    liked_by = created_proposal.liked_by.all()
    assert_that(liked_by, has_length(1))
    assert_that(liked_by.first().id, equal_to(fanboy.id))


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_like_proposal(client):
    subject = "anything"
    password = "Password10!"
    description = "Any description"
    proposer = UserBuilder().with_email("a@a.com").build()
    fanboy = UserBuilder().with_email("b@b.com").with_password(password).build()
    topic = TopicBuilder().build()
    proposal = (
        ProposalBuilder()
        .with_subject(subject)
        .with_description(description)
        .with_topics([topic])
        .with_proposed_by(proposer)
        .build()
    )
    url = reverse_lazy("api-alpha:like_proposal", kwargs={"proposal_id": proposal.id})
    client.login(username=fanboy.email, password=password)

    response = client.put(url, data={}, content_type="application/json")

    assert_that(response.status_code, equal_to(HTTPStatus.NO_CONTENT))
    liked_by = proposal.liked_by.all()
    assert_that(liked_by, has_length(1))
    assert_that(liked_by.first().id, equal_to(fanboy.id))


@freeze_time("2022-10-26 23:23:23")
@pytest.mark.django_db
def test_unlike_proposal(client):
    subject = "anything"
    password = "Password10!"
    description = "Any description"
    proposer = UserBuilder().with_email("a@a.com").build()
    fanboy = UserBuilder().with_email("b@b.com").with_password(password).build()
    topic = TopicBuilder().build()
    proposal = (
        ProposalBuilder()
        .with_subject(subject)
        .with_description(description)
        .with_topics([topic])
        .with_proposed_by(proposer)
        .with_liked_by([fanboy])
        .build()
    )
    url = reverse_lazy("api-alpha:like_proposal", kwargs={"proposal_id": proposal.id})
    client.login(username=fanboy.email, password=password)

    response = client.delete(url, data={}, content_type="application/json")

    assert_that(response.status_code, equal_to(HTTPStatus.NO_CONTENT))
    liked_by = proposal.liked_by.all()
    assert_that(liked_by, has_length(0))
