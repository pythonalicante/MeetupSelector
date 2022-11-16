import pytest
from django.urls import reverse

from meetupselector.api.api import api


@pytest.fixture(scope="session")
def celery_config():
    return {
        "task_always_eager": True,
        "task_eager_propagates": True,
        "broker_url": "memory://",
        "result_backend": "file:///tmp",
    }


@pytest.fixture
def reverse_url():
    def _reverse_url(function_name: str, kwargs: dict | None = None) -> str:
        api_namespace = api.urls_namespace

        return reverse(f"{api_namespace}:{function_name}", kwargs=kwargs)

    return _reverse_url
