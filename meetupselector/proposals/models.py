import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from meetupselector.talks.models import TalkDifficulty as Difficulty


class Language(models.TextChoices):
    EN_GB = "EN_GB", _("english")
    FR_FR = "FR_FR", _("french")
    ES_ES = "ES_ES", _("spain")
    ES_EU = "ES_EU", _("basque")
    ES_CA = "ES_CA", _("catalonian")
    ES_GL = "ES_GL", _("galicia")


class Proposal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=255, verbose_name=_("subjects"))
    description = models.TextField(verbose_name=_("description"))
    difficulty = models.CharField(
        verbose_name=_("difficulty"),
        max_length=1,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    language = models.CharField(
        verbose_name=_("language"),
        max_length=6,
        choices=Language.choices,
        default=Language.ES_ES,
    )
    topics = models.ManyToManyField(
        "talks.Topic",
        verbose_name=_("topics"),
        related_name="proposals",
    )
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("proposed_by"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="proposal",
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("liked_by"),
        related_name="proposals",
        blank=True,
    )
    done = models.BooleanField(
        default=False,
        verbose_name=_("done"),
    )

    class Meta:
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def __str__(self) -> str:
        return self.subject


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    location = models.CharField(max_length=255, verbose_name=_("location"))
    meetup_link = models.CharField(max_length=255, verbose_name=_("meetup_link"))
    done = models.BooleanField(
        default=False,
        verbose_name=_("done"),
    )

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self) -> str:
        return self.name
