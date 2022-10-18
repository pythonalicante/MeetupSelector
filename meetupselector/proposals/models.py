from email.policy import default
from random import choices
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Difficulty(models.TextChoices):
    EASY = "E", _("easy")
    MEDIUM = "M", _("medium")
    HARD = "H", _("hard")


class Language(models.TextChoices):
    EN_GB = "EN", _("english")
    FR_FR = "FR", _("french")
    ES_ES = "ES_ES", _("spain")
    ES_EU = "ES_EU", _("basque")
    ES_CA = "ES_CA", _("catalonian")
    ES_GL = "ES_GL", _("galicia")

class Proposal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(verbose_name=_("description"))
    difficulty = models.CharField(
        verbose_name= _("difficulty"),
        max_length=1,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )

