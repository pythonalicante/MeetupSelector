from abc import ABC, abstractmethod

from django.db.models import Model


class ResourceBuilder(ABC):
    @abstractmethod
    def build(self) -> Model:
        raise NotImplementedError
