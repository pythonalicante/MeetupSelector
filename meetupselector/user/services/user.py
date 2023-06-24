from urllib.parse import urljoin
from uuid import UUID

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import Http404, HttpRequest
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from pydantic import UUID4

from ..models import User
from ..tasks import send_registration_mail, send_reset_password_email
from ..token import token_generator


def login(request: HttpRequest, email: str, password: str) -> AbstractBaseUser | None:
    user = authenticate(username=email, password=password)
    if user is None:
        return None

    django_login(request, user)
    return user


def create(email: str, password: str, GDPR_accepted: bool, request: HttpRequest):
    new_user = User.objects.create_user(
        email=email,
        password=password,
        GDPR_accepted=GDPR_accepted,
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


def reset_password_email(email: str):
    User = get_user_model()

    try:
        user = User.objects.get(email=email)
        send_reset_password_email(user.pk)
        return 200
    except User.DoesNotExist as e:
        raise Http404(_("User not found"))


def reset_password(uidb64, token, new_password):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return 200
    else:
        raise Http404(_("User not found"))
