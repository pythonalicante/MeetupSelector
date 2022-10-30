import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TalkType(models.TextChoices):
    TALK = "T", _("talk")
    WORKSHOP = "W", _("workshop")
    KATA = "K", _("kata")


class TalkDifficulty(models.TextChoices):
    EASY = "E", _("easy")
    MEDIUM = "M", _("medium")
    HARD = "H", _("hard")


# Create your models here.
class Topic(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(verbose_name=_("name"), max_length=255)
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self) -> str:
        return f"{self.name}"
