from http import HTTPStatus

from ninja import Router

from meetupselector.api.schemas.users import LoginSchema
from meetupselector.user.services import AuthenticationService

router = Router()


@router.post("/login", response={HTTPStatus.OK: None, HTTPStatus.UNAUTHORIZED: None}, auth=None)
def login(request, credentials: LoginSchema, auth=None):
    user = AuthenticationService.login(
        email=credentials.email,
        password=credentials.password,
    )
    if user is None:
        return HTTPStatus.UNAUTHORIZED, None
    else:
        return HTTPStatus.OK, None
