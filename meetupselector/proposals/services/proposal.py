from typing import List

from django.contrib.auth import get_user_model
from pydantic import UUID4

from ..models import Proposal

User = get_user_model()


def create(
    subject: str,
    description: str,
    difficulty: str,
    language: str,
    topics: List[UUID4],
    talks: List[UUID4],
    proposed_by: UUID4,
    liked_by: List[UUID4],
    done: bool,
) -> Proposal:
    proposal = Proposal(
        subject=subject,
        description=description,
        difficulty=difficulty,
        language=language,
        proposed_by=User.objects.get(pk=proposed_by),
        done=done,
    )
    proposal.save()
    for _topic in topics:
        proposal.topics.add(_topic)  # type: ignore
    for _talk in talks:
        proposal.talks.add(_talk)  # type: ignore
    for _user in liked_by:
        proposal.liked_by.add(_user)  # type: ignore

    return proposal
