from django.db.models import QuerySet
from pydantic import UUID4

from ..models import Talk


def list() -> QuerySet[Talk]:
    return Talk.objects.all()


def get(talk_id: UUID4) -> Talk:
    return Talk.objects.get(id=talk_id)
