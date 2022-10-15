from ninja import NinjaAPI

from .routes import proposals_router, talks_router, users_router

api = NinjaAPI(
    title="MeetupSelector API",
    version="alpha",
    description="API for project https://github.com/pythonalicante/MeetupSelector/",
)

api.add_router("/proposals_app/", proposals_router, tags=["Proposals"])
api.add_router("/talks_app/", talks_router, tags=["Talks"])
api.add_router("/users_app/", users_router, tags=["Users"])


@api.get("/healthcheck", tags=["Healthchecks"])
def healthcheck(_):
    return {"healthy": True}
