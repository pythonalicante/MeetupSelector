import typing as t
import uuid

from django.core.exceptions import PermissionDenied
from django.db import models


class UUIDPkMixin(models.Model):
    """Mixin that set as primary key an UUIDv4.

    The primary key is auto filled and it isn't editable.

    Attributes
    ----------
    id : uuid4
        The primary key of the model
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    """Mixin that set timestamps for now when a model is created or updated.

    The attributes are populated automatically.

    Attributes
    ----------
    created_at : datetime
        When the model is created. This field is not editable.
    updated_at : datetime
        When the model is updated.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProtectedMixin(models.Model):
    """Mixin that checks if the model is protected and disable delete if it's protected.

    Attributes
    ----------
    protected : boolean
        True if the model is protected.

    """

    protected: models.BooleanField = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs) -> t.Tuple[int, t.Dict[str, int]]:
        """Overrides delete method of the model.

        Parameters
        ----------
        *args
            Parent arguments
        **kwargs
            Parent keyword arguments

        Raises
        ------
        AppException
            If the model is protected.
        """
        if self.protected:
            raise PermissionDenied(f"Can't delete '{self}' due to it's protected")
        return super().delete(*args, **kwargs)


class CleanSaveMixin(models.Model):
    """Mixin that overrides the `save` method to call `full_clean()`."""

    class Meta:
        abstract = True

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        full_clean=True,
    ):
        """Overrides save method of the model.

        Parameters
        ---------
        force_insert : bool
        force_update : bool
        using : str, optional
        update_fields : bool, optional
        full_clean : bool, default
            If this parameter is True (by default), the `full_clean` method of the model is called.
        """
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

        if full_clean:
            self.full_clean()


class AppModel(
    UUIDPkMixin,
    TimeStampMixin,
    ProtectedMixin,
    CleanSaveMixin,
    models.Model,
):
    class Meta:
        abstract = True
