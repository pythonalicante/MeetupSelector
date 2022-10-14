from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from meetupselector.api.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

if settings.DEBUG:
    import warnings

    try:
        import debug_toolbar  # noqa: F401
    except ImportError:
        warnings.warn(
            "The debug toolbar was not installed. Ignore the error. \
            settings.py should already have warned the user about it."
        )
    else:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),  # type: ignore
        ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
