from ninja import Field, ModelSchema
from pydantic import UUID4

from meetupselector.proposals.models import Event, Proposal

from .talks import TopicRetrieveSchema


class ProposalCreateSchema(ModelSchema):
    topics: list[UUID4] | None = None
    proposed_by: UUID4
    liked_by: list[UUID4] | None = None

    class Config:
        model = Proposal
        model_fields = [
            "subject",
            "description",
            "difficulty",
            "language",
            "done",
        ]


class ProposalRetrieveSchema(ModelSchema):
    topics: list[TopicRetrieveSchema]

    class Config:
        model = Proposal
        model_fields = [
            "id",
            "created_at",
            "updated_at",
            "subject",
            "description",
            "difficulty",
            "language",
            "proposed_by",
            "liked_by",
            "done",
        ]


class ProposalListSchema(ModelSchema):
    topics: list[TopicRetrieveSchema]
    likes: int = Field(default=0, alias="likes", read_only=True)

    class Config:
        model = Proposal
        model_fields = [
            "id",
            "created_at",
            "updated_at",
            "subject",
            "difficulty",
            "language",
        ]


class EventCreateSchema(ModelSchema):
    class Config:
        model = Event
        model_fields = [
            "name",
            "description",
            "meetup_link",
            "location",
            "date",
            "start_time",
            "duration",
        ]


class EventRetrieveSchema(ModelSchema):
    duration: int = Field(alias="duration_seconds")

    class Config:
        model = Event
        model_fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "description",
            "meetup_link",
            "location",
            "date",
            "start_time",
        ]


class EventListSchema(ModelSchema):
    duration: int = Field(alias="duration_seconds")

    class Config:
        model = Event
        model_fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "description",
            "meetup_link",
            "location",
            "date",
            "start_time",
        ]
