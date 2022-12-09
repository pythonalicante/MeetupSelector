from urllib.parse import urljoin
from uuid import UUID

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import Http404, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
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


def create(signin_data: SignInSchema, request: HttpRequest):
    new_user = User.objects.create_user(
        email=signin_data.email,
        password=signin_data.password,
        GDPR_accepted=signin_data.GDPR_accepted,
        is_active=False,
    )
    api_namespace = settings.API_NAMESPACE
    confirmation_url_path = reverse(
        f"{api_namespace}:{settings.CONFIRMATION_URL_NAME}", kwargs={"user_id": new_user.id}
    )
    confirmation_url = request.build_absolute_uri(confirmation_url_path)

    confirmation_url = urljoin(f"{confirmation_url}/", str(new_user.id))
    send_registration_mail.delay(email=new_user.email, confirmation_url=confirmation_url)


def delete(user_id: UUID4):
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return 200
    except User.DoesNotExist:
        raise Http404(_("User not found"))


def activate(user_id: str) -> User | None:
    user = None
    try:
        uid = UUID(user_id)
        user = User.objects.filter(id=uid).first()
    except ValueError:
        pass
    if user is not None:
        user.is_active = True
        user.save()
    return user
