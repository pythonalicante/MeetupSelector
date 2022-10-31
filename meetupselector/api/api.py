from ninja import NinjaAPI

from .routes import proposals_router, topics_router, users_router

api = NinjaAPI(
    title="MeetupSelector API",
    version="alpha",
    description="API for project https://github.com/pythonalicante/MeetupSelector/",
    csrf=True,
)

api.add_router("/proposals/", proposals_router, tags=["Proposals"])
api.add_router("/topics/", topics_router, tags=["Topics"])
api.add_router("/users/", users_router, tags=["Users"])


@api.get("/healthcheck", tags=["Healthchecks"])
def healthcheck(_):
    return {"healthy": True}
