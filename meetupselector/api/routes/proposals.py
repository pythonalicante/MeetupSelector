import typing as t

from ninja import Router
from ninja.security import django_auth
from pydantic import UUID4

from meetupselector.api.schemas.proposals import (
    ProposalCreateSchema,
    ProposalListSchema,
    ProposalRetrieveSchema,
)
from meetupselector.proposals.services import ProposalService

router = Router(auth=django_auth)


@router.post(
    "/proposal", response={201: ProposalRetrieveSchema}, url_name="create_list_proposal", auth=None
)
def create_proposal(request, proposal: ProposalCreateSchema):
    return 201, ProposalService.create(**proposal.dict())


@router.put(
    "/proposal/{proposal_id}/like",
    response={204: None},
    url_name="like_proposal",
)
def like_proposal(request, proposal_id: UUID4):
    user = request.auth
    ProposalService.like(proposal_id, user.id)
    return 204, None


@router.delete(
    "/proposal/{proposal_id}/like",
    response={204: None},
    url_name="like_proposal",
)
def unlike_proposal(request, proposal_id: UUID4):
    user = request.auth
    ProposalService.unlike(proposal_id, user.id)
    return 204, None

    
@router.get("/proposal", response={200: t.List[ProposalListSchema]}, url_name="list_proposals")
def list_proposals(request):
    return 200, ProposalService.retrieve_all()
