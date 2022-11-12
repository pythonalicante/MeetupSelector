import typing as t

from ninja import Router
from ninja.security import django_auth
from pydantic import UUID4

from meetupselector.api.schemas.proposals import (
    EventCreateSchema,
    EventListSchema,
    EventRetrieveSchema,
    ProposalCreateSchema,
    ProposalListSchema,
    ProposalRetrieveSchema,
)
from meetupselector.proposals.services import ProposalService

router = Router(auth=django_auth)


@router.get(
    "/",
    response={200: t.List[ProposalListSchema]},
    url_name="create_list_proposal",
    auth=None,
)
def list_proposals(request):
    return 200, ProposalService.retrieve_all()


@router.post("/", response={201: ProposalRetrieveSchema}, auth=None)
def create_proposal(request, proposal: ProposalCreateSchema):
    return 201, ProposalService.create(**proposal.dict())


@router.put(
    "/{proposal_id}/like",
    response={204: None},
    url_name="like_proposal",
)
def like_proposal(request, proposal_id: UUID4):
    user = request.auth
    ProposalService.like(proposal_id, user.id)
    return 204, None


@router.delete(
    "/{proposal_id}/like",
    response={204: None},
    url_name="like_proposal",
)
def unlike_proposal(request, proposal_id: UUID4):
    user = request.auth
    ProposalService.unlike(proposal_id, user.id)
    return 204, None


@router.get(
    "/event",
    response={200: t.List[EventListSchema]},
    url_name="create_list_event",
    auth=None,
)
def list_events(request):
    return 200, EventService.retrieve_all()


@router.post(
    "/event",
    response={201: EventRetrieveSchema, 401: None},
    url_name="create_list_event",
)
def create_event(request, event: EventCreateSchema):
    user = request.user
    if user.is_staff:
        return 201, EventService.create(**event.dict())
    return 401, None
