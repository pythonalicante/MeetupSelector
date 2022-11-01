from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


def login(request: HttpRequest, email: str, password: str) -> AbstractBaseUser | None:
    user = authenticate(username=email, password=password)
    if user is None:
        return None

    django_login(request, user)
    return user
