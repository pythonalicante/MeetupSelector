from http import HTTPStatus

from django.conf import settings
from django.urls import reverse
from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.users import LoginSchema
from meetupselector.user.schemas import SignInSchema
from meetupselector.user.services import UserService

confirmation_url_name = "signin_confirmation"

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
def create_user(_, credentials: SignInSchema):
    api_namespace = settings.API_NAMESPACE
    confirmation_url = reverse(f"{api_namespace}:{confirmation_url_name}")
    return HTTPStatus.CREATED, UserService.create(credentials, confirmation_url)


@router.get(
    "/signin_confirmation",
    response={HTTPStatus.OK: None},
    url_name=confirmation_url_name,
    auth=None,
)
def activate_user(_):
    # TODO: Activate user and redirect to main page
    return HTTPStatus.OK, None
