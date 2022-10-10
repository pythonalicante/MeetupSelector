import warnings

from .default import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

INTERNAL_IPS = ["127.0.0.1"]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]


try:
    __import__("debug_toolbar")
except ImportError as exc:
    msg = (
        f"{exc} -- Install the missing dependencies by "
        f"running `pip install -r requirements.txt`"
    )
    warnings.warn(msg)  # noqa
else:
    INSTALLED_APPS += ["debug_toolbar"]  # noqa
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
    DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 100}
