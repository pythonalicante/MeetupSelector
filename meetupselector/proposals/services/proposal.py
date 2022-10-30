from typing import List

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from pydantic import UUID4

from ..models import Proposal

User = get_user_model()


def create(
    subject: str,
    description: str,
    difficulty: str,
    language: str,
    topics: List[UUID4],
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
    for _user in liked_by:
        proposal.liked_by.add(_user)  # type: ignore

    return proposal


def retrieve_all() -> QuerySet[Proposal]:
    return Proposal.objects.all()


def like(proposal_id: UUID4, user_id: UUID4):
    user = get_object_or_404(User, pk=user_id)
    proposal_to_like = get_object_or_404(Proposal, pk=proposal_id)
    if user not in proposal_to_like.liked_by.all():
        proposal_to_like.liked_by.add(user)


def unlike(proposal_id: UUID4, user_id: UUID4):
    user = get_object_or_404(User, pk=user_id)
    proposal_to_like = get_object_or_404(Proposal, pk=proposal_id)
    if user in proposal_to_like.liked_by.all():
        proposal_to_like.liked_by.remove(user)
