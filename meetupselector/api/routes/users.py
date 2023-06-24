from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from ninja import Router
from ninja.security import django_auth

from meetupselector.api.schemas.users import (
    LoginSchema,
    ResetPasswordSchema,
    SignUpSchema,
    UserPasswordChangeSchema,
)
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
def create_user(request: HttpRequest, credentials: SignUpSchema):
    return HTTPStatus.CREATED, UserService.create(
        email=credentials.email,
        password=credentials.password,
        GDPR_accepted=credentials.GDPR_accepted,
        request=request,
    )


@router.get(
    "/signup_confirmation/{user_id}",
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


@router.post(
    "/reset_password_link",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: None, HTTPStatus.UNAUTHORIZED: None},
    url_name="reset_password_link",
    auth=None,
)
def reset_password_email(_, credentials: ResetPasswordSchema):
    return UserService.reset_password_email(email=credentials.email)


@router.post(
    "/reset_password/{uidb64}/{token}",
    url_name="reset_password",
    response={HTTPStatus.OK: None, HTTPStatus.NOT_FOUND: None, HTTPStatus.UNAUTHORIZED: None},
    auth=None,
)
def reset_password(_, uidb64, token, data: UserPasswordChangeSchema):
    return UserService.reset_password(uidb64, token, new_password=data.new_password)
