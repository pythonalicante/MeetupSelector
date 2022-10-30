from uuid import uuid4

from ninja import ModelSchema, Schema
from pydantic import UUID4

from meetupselector.proposals.models import Proposal
from meetupselector.proposals.services.proposal import like

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
            "topics",
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
            "proposed_by",
            "liked_by",
            "done",
        ]


class ProposalLikeSchema(Schema):
    ok: bool = False
