from meetupselector.talks.models import Topic


class TopicBuilder:
    _name: str = "topic"
    _description: str = "description"

    def with_name(self, name) -> "TopicBuilder":
        self._name = name
        return self

    def with_description(self, description: str) -> "TopicBuilder":
        self._description = description
        return self

    def build(self) -> Topic:
        return Topic.objects.create(
            name=self._name,
            description=self._description,
        )
