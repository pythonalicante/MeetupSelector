from meetupselector.talks.models import Topic
from tests.utils.builders.interface import ResourceBuilder


class TopicBuilder(ResourceBuilder):
    def with_name(self, name: str) -> "TopicBuilder":
        self._name = name
        return self

    def with_default_description(self) -> "TopicBuilder":
        self._description = "Test Topic Description"
        return self

    def with_description(self, description: str) -> "TopicBuilder":
        self._description = description
        return self

    def build(self) -> Topic:
        if not getattr(self, "_name", None):
            raise ValueError("You should call `with_name(name)` method.")
        if not getattr(self, "_description", None):
            self = self.with_default_description()
        _topic = Topic(name=self._name, description=self._description)
        _topic.save()
        return _topic
