import logging

from ninja import ModelSchema, Schema
from pydantic import UUID4

from meetupselector.talks.models import Talk, Topic

logger = logging.getLogger(__name__)


class TopicListSchema(ModelSchema):
    class Config:
        model = Topic
        model_fields = ["id", "name"]


class TopicRetrieveSchema(ModelSchema):
    class Config:
        model = Topic
        model_fields = ["id", "name", "description", "created_at", "updated_at"]


class TalkListSchema(ModelSchema):
    class Config:
        model = Talk
        model_fields = ["id", "name", "headline", "type", "created_at", "updated_at"]


class TalkRetrieveSchema(ModelSchema):
    topics: list[TopicRetrieveSchema]

    class Config:
        model = Talk
        model_fields = [
            "id",
            "name",
            "headline",
            "description",
            "duration",
            "type",
            "difficulty",
            "topics",
            "created_at",
            "updated_at",
        ]


class TalkCreateSchema(ModelSchema):
    topics: list[UUID4]

    class Config:
        model = Talk
        model_fields = [
            "name",
            "headline",
            "description",
            "duration",
            "type",
            "difficulty",
            "topics",
        ]


class TalkUpdateSchema(Schema):
    id: UUID4
    name: str = None
    headline: str = None
    description: str = None
    duration: int = None
    type: str = None
    difficulty: str = None
    topics: list[UUID4] = None
