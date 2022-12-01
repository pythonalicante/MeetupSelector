from http import HTTPStatus

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import Http404, HttpRequest
from django.utils.translation import gettext_lazy as _
from pydantic import UUID4

from ..models import User
from ..schemas import SignInSchema
from ..tasks import send_registration_mail


def login(request: HttpRequest, email: str, password: str) -> AbstractBaseUser | None:
    user = authenticate(username=email, password=password)
    if user is None:
        return None

    django_login(request, user)
    return user


def create(signin_data: SignInSchema, confirmation_url: str):
    new_user = User.objects.create_user(
        email=signin_data.email,
        password=signin_data.password,
        GDPR_accepted=signin_data.GDPR_accepted,
        is_active=False,
    )
    send_registration_mail.delay(email=new_user.email, confirmation_url=confirmation_url)


def delete(user_id: UUID4):
    """Delete user account.

    :param account_id:
    :type account_id: UUID4
    :param user_id:
    :type user_id: UUID4
    """
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return 200
    except User.DoesNotExist as e:
        raise Http404(_("User not found"))
