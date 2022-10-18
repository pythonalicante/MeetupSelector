from django.db.models import QuerySet
from pydantic import UUID4

from ..models import Topic


def list() -> QuerySet[Topic]:
    return Topic.objects.all()


def get(topic_id: UUID4) -> Topic:
    return Topic.objects.get(id=topic_id)
