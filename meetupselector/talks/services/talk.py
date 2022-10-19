import logging
import typing as t

from django.db.models import QuerySet
from pydantic import UUID4

from ..models import Talk

logger = logging.getLogger(__name__)


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


def update(
    *,
    id: UUID4,
    name: str,
    headline: str,
    description: str,
    duration: int,
    type: str,
    difficulty: str,
    topics: t.List[UUID4],
) -> Talk:
    logger.debug("LLEGO")
    _talk: Talk = Talk.objects.get(id=id)
    if name:
        _talk.name = name
    if headline:
        _talk.headline = headline
    if description:
        _talk.description = description
    if duration:
        _talk.duration = duration
    if type:
        _talk.type = type
    if difficulty:
        _talk.difficulty = difficulty
    _talk.save()
    if topics:
        _talk.topics.clear()
        for _topic in topics:
            _talk.topics.add(_topic)  # type: ignore
    return _talk
