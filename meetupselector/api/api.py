from django.conf import settings
from ninja import NinjaAPI

from .routes import events_router, proposals_router, topics_router, users_router

api = NinjaAPI(
    title="MeetupSelector API",
    version=settings.API_VERSION,
    description="API for project https://github.com/pythonalicante/MeetupSelector/",
    csrf=True,
    urls_namespace=settings.API_NAMESPACE,
)

api.add_router("/events/", events_router, tags=["Events"])
api.add_router("/proposals/", proposals_router, tags=["Proposals"])
api.add_router("/topics/", topics_router, tags=["Topics"])
api.add_router("/users/", users_router, tags=["Users"])


@api.get("/healthcheck", tags=["Healthchecks"])
def healthcheck(_):
    return {"healthy": True}
