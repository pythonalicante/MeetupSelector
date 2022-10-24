from ninja import ModelSchema
from pydantic import UUID4

from .talks import TopicRetrieveSchema
from meetupselector.proposals.models import Proposal


class ProposalCreateSchema(ModelSchema):
    topics: list[UUID4]
    talks: list[UUID4]
    proposed_by: UUID4
    liked_by: list[UUID4]

    class Config:
        model = Proposal
        model_fields = [
            "subject",
            "description",
            "difficulty",
            "language",
            "topics",
            "talks",
            "proposed_by",
            "liked_by",
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
            "topics",
            "talks",
            "proposed_by",
            "liked_by",
            "done",
        ]
