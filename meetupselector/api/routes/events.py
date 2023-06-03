import typing as t

from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.proposals import (
    EventCreateSchema,
    EventListSchema,
    EventRetrieveSchema,
)
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


@router.get(
    "/",
    response={200: t.List[EventListSchema]},
    url_name="create_list_event",
    auth=None,
)
def list_events(request):
    return 200, EventService.retrieve_all()
