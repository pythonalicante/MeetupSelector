from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.proposals import EventCreateSchema, EventRetrieveSchema
from meetupselector.proposals.services import EventService

router = Router(auth=django_auth)


@router.post(
    "/",
    response={201: EventRetrieveSchema, 401: None},
    url_name="event",
)
def create_event(request, event: EventCreateSchema):
    user = request.user
    if user.is_staff:
        return 201, EventService.create(**event.dict())
    return 401, None
