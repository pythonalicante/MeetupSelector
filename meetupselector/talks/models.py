from django.db import models
from django.utils.translation import gettext_lazy as _

from meetupselector.shared.db.models import AppModel


class TalkType(models.TextChoices):
    TALK = "T", _("talk")
    WORKSHOP = "W", _("workshop")
    KATA = "K", _("kata")


class TalkDifficulty(models.TextChoices):
    EASY = "E", _("easy")
    MEDIUM = "M", _("medium")
    HARD = "H", _("hard")


# Create your models here.
class Talk(AppModel):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    headline = models.CharField(verbose_name=_("headline"), max_length=255)
    description = models.TextField(verbose_name=_("description"))
    duration = models.DurationField(verbose_name=_("duration"))
    type = models.CharField(
        verbose_name=_("type"), max_length=1, choices=TalkType.choices, default=TalkType.TALK
    )
    difficulty = models.CharField(
        verbose_name=_("difficulty"),
        max_length=1,
        choices=TalkDifficulty.choices,
        default=TalkDifficulty.EASY,
    )
    slides = models.URLField(verbose_name=_("slides"), blank=True, null=True)
    repository = models.URLField(verbose_name=_("repository"), blank=True, null=True)

    class Meta:
        verbose_name = _("talk")
        verbose_name_plural = _("talks")

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.name}"
