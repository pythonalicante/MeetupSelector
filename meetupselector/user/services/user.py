from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

from ..models import User


def login(request: HttpRequest, email: str, password: str) -> AbstractBaseUser | None:
    user = authenticate(username=email, password=password)
    if user is None:
        return None

    django_login(request, user)
    return user


def create(email: str, password: str):
    user = User.objects.create(email=email, is_active=False)
    user.set_password(password)
    user.save()
