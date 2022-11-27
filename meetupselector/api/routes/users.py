from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from kombu.utils.functional import accepts_argument
from ninja import Router
from ninja.security import django_auth
from pydantic import UUID4

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
    api_namespace = settings.API_NAMESPACE
    confirmation_url_path = reverse(f"{api_namespace}:{settings.CONFIRMATION_URL_NAME}")
    confirmation_url = request.build_absolute_uri(confirmation_url_path)

    return HTTPStatus.CREATED, UserService.create(credentials, confirmation_url)


@router.get(
    "/signin_confirmation",
    response={HTTPStatus.OK: None},
    url_name=settings.CONFIRMATION_URL_NAME,
    auth=None,
)
def activate_user(_):
    # TODO: Activate user and redirect to main page
    return HTTPStatus.OK, None


@router.delete(
    "/delete_user/{account_id}",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: None, HTTPStatus.UNAUTHORIZED: None},
    url_name="delete_user",
)
def delete_user(request, account_id: UUID4):
    user = request.auth
    return UserService.delete(account_id=account_id, user_id=user.id)
