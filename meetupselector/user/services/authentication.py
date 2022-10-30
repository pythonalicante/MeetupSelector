from django.contrib.auth import authenticate

from meetupselector.user.models import User


def login(email: str, password: str) -> User | None:
    return authenticate(username=email, password=password)
