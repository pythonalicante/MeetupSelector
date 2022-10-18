import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Difficulty(models.TextChoices):
    EASY = "E", _("easy")
    MEDIUM = "M", _("medium")
    HARD = "H", _("hard")


class Language(models.TextChoices):
    ES_ES = "ES_ES", _("spanish")
    ES_CA = "ES_CA", _("catalonian")
    ES_GL = "ES_GL", _("galician")
    ES_EU = "ES_EU", _("basque")
    EN_GB = "ES_GB", _("english")
    FR_FR = "FR_FR", _("french")


class Proposal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(verbose_name=_("description"))
    difficulty = models.CharField(
        verbose_name=_("difficulty"),
        max_length=1,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    language = models.CharField(
        verbose_name=_("language"),
        max_length=5,
        choices=Language.choices,
        default=Language.ES_ES,
    )
    topics = models.ManyToManyField(
        'talks.Topic',
        verbose_name=_("topics"),
        related_name="proposals",
    )
    talks = models.ManyToManyField(
        'talks.Talk',
        verbose_name=_("talks"),
        related_name="proposals",
    )
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name=_("proposal"),
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("liked_by"),
        related_name="proposal_votes",
    )
    done = models.BooleanField(
        default=False,
        verbose_name=_("done"),
    )

    class Meta:
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.name}"