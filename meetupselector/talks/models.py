import uuid

from django.conf import settings
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


class Speaker(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name=_("speaker"), null=True
    )
    contact_email = models.EmailField(verbose_name=_("contact_email"))
    city = models.CharField(verbose_name=_("city"), max_length=255)
    webpage = models.URLField(verbose_name=_("webpage"), blank=True, null=True)
    social_networks = models.JSONField(verbose_name=_("social_networks"), default=dict, blank=True)

    class Meta:
        verbose_name = _("speaker")
        verbose_name_plural = _("speakers")

    def __str__(self) -> str:
        return f"[{self.city}] {self.contact_email}"


class Talk(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    speakers = models.ManyToManyField(to=Speaker, related_name="talks", verbose_name=_("speakers"))
    topics = models.ManyToManyField(to=Topic, verbose_name=_("topics"), related_name="talks")

    class Meta:
        verbose_name = _("talk")
        verbose_name_plural = _("talks")

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.name}"
