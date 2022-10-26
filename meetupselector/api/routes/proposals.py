from ninja import Router

from meetupselector.api.schemas.proposals import (
    ProposalCreateSchema,
    ProposalRetrieveSchema,
)
from meetupselector.proposals.services import ProposalService

router = Router()


@router.post("/proposal", response={201: ProposalRetrieveSchema}, url_name="create_list_proposal")
def create_proposal(request, proposal: ProposalCreateSchema):
    return 201, ProposalService.create(**proposal.dict())
