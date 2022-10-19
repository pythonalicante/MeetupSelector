import typing as t

from django.db.models import QuerySet
from pydantic import UUID4

from ..models import Talk


def list() -> QuerySet[Talk]:
    return Talk.objects.all()


def get(talk_id: UUID4) -> Talk:
    return Talk.objects.get(id=talk_id)


def create(
    name: str,
    headline: str,
    description: str,
    duration: int,
    type: str,
    difficulty: str,
    topics: t.List[UUID4],
) -> Talk:
    _talk = Talk(
        name=name,
        headline=headline,
        description=description,
        duration=duration,
        type=type,
        difficulty=difficulty,
    )
    _talk.save()
    for _topic in topics:
        _talk.topics.add(_topic)  # type: ignore
    return _talk
