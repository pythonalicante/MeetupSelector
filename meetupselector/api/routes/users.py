from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.users import LoginSchema
from meetupselector.user.schemas import SignInSchema
from meetupselector.user.services import UserService

router = Router(auth=django_auth)


@router.post("/login", response={HTTPStatus.OK: None, HTTPStatus.UNAUTHORIZED: None}, auth=None)
def login(request, credentials: LoginSchema, auth=None):
    user = UserService.login(
        request=request,
        email=credentials.email,  # type: ignore
        password=credentials.password,  # type: ignore
    )
    if user is None:
        return HTTPStatus.UNAUTHORIZED, None
    return HTTPStatus.OK, None


@router.post("/users", response={HTTPStatus.CREATED: None}, url_name="create_user", auth=None)
def create_user(request: HttpRequest, credentials: SignInSchema):
    return HTTPStatus.CREATED, UserService.create(credentials, request)


@router.get(
    "/signin_confirmation/{user_id}",
    response={HTTPStatus.FOUND: None} | {HTTPStatus.NOT_FOUND: None},
    url_name=settings.CONFIRMATION_URL_NAME,
    auth=None,
)
def activate_user(request: HttpRequest, user_id: str, response: HttpResponse):
    user = UserService.activate(user_id)
    if user is None:
        return HTTPStatus.NOT_FOUND, None

    base_url = request.build_absolute_uri().replace(request.get_full_path(), "/")
    response["Location"] = base_url

    return HTTPStatus.FOUND, None  # 302 redirect


@router.delete(
    "/",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: None, HTTPStatus.UNAUTHORIZED: None},
    url_name="/",
)
def delete_user(request):
    user = request.auth
    return UserService.delete(user_id=user.id)
