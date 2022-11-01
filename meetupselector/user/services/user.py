from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

from ..models import User
from ..schemas import SignInSchema


def login(request: HttpRequest, email: str, password: str) -> AbstractBaseUser | None:
    user = authenticate(username=email, password=password)
    if user is None:
        return None

    django_login(request, user)
    return user


def create(signin_data: SignInSchema):
    User.objects.create_user(
        email=signin_data.email,
        password=signin_data.password,
        is_active=False,
    )
