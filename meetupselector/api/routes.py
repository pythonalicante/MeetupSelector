"""API Django Ninja endpoints.

Feel free to import all needed models and/or application services from
project applications.
"""
from ninja import NinjaAPI


api = NinjaAPI()


@api.get("/healthcheck")
def healthcheck(_):
    return {"healthy": True}
