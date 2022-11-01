from http import HTTPStatus

from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.users import LoginSchema, SignInSchema
from meetupselector.user.services import UserService

router = Router(auth=django_auth)


@router.post("/login", response={HTTPStatus.OK: None, HTTPStatus.UNAUTHORIZED: None}, auth=None)
def login(request, credentials: LoginSchema, auth=None):
    user = UserService.login(
        request=request,
        email=credentials.email,
        password=credentials.password,
    )
    if user is None:
        return HTTPStatus.UNAUTHORIZED, None
    else:
        return HTTPStatus.OK, None


@router.post("/users", response={HTTPStatus.CREATED: None}, url_name="create_user", auth=None)
def create_user(_, credentials: SignInSchema):
    return HTTPStatus.CREATED, UserService.create(**credentials.dict())
