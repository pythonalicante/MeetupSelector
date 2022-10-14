from ninja import NinjaAPI

from .routes import proposals_router, talks_router, users_router

api = NinjaAPI()

api.add_router("/proposals_app/", proposals_router)
api.add_router("/talks_app/", talks_router)
api.add_router("/users_app/", users_router)


@api.get("/healthcheck")
def healthcheck(_):
    return {"healthy": True}
