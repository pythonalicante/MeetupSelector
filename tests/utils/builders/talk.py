from meetupselector.talks.models import Talk
from tests.utils.builders.interface import ResourceBuilder


class TalkBuilder(ResourceBuilder):
    def with_name(self, name: str) -> "TalkBuilder":
        self._name = name
        return self

    def with_default_description(self) -> "TalkBuilder":
        self._description = "Test Talk Description"
        return self

    def with_description(self, description: str) -> "TalkBuilder":
        self._description = description
        return self

    def with_headline(self, headline) -> "TalkBuilder":
        self._headline = headline
        return self

    def with_duration(self, duration) -> "TalkBuilder":
        self._duration = duration
        return self

    def with_type(self, type) -> "TalkBuilder":
        self._type = type
        return self

    def with_difficulty(self, difficulty) -> "TalkBuilder":
        self._difficulty = difficulty
        return self

    def with_slides(self, slides) -> "TalkBuilder":
        self._slides = slides
        return self

    def with_repository(self, repository) -> "TalkBuilder":
        self._repository = repository
        return self

    def with_speaker(self, speaker) -> "TalkBuilder":
        if not getattr(self, "_speakers", None):
            self._speakers = []
        self._speakers.append(speaker)
        return self

    def with_topic(self, topic) -> "TalkBuilder":
        if not getattr(self, "_topics", None):
            self._topics = []
        self._topics.append(topic)
        return self

    def _validate_input(self) -> "TalkBuilder":
        if not getattr(self, "_name", None):
            raise ValueError("You should call `with_name(name)` method.")
        if not getattr(self, "_headline", None):
            raise ValueError("You should call `with_headline(headline)` method.")
        if not getattr(self, "_description", None):
            self = self.with_default_description()
        if not getattr(self, "_duration", None):
            raise ValueError("You should call `with_duration(duration)` method.")
        if not getattr(self, "_type", None):
            raise ValueError("You should call `with_type(type)` method.")
        if not getattr(self, "_difficulty", None):
            raise ValueError("You should call `with_difficulty(difficulty)` method.")
        if not getattr(self, "_slides", None):
            self._slides = None
        if not getattr(self, "_repository", None):
            self._repository = None
        if not getattr(self, "_speakers", None):
            self._speakers = []
        if not getattr(self, "_topics", None):
            self._topics = []
        return self

    def build(self) -> Talk:
        self = self._validate_input()
        _talk = Talk(
            name=self._name,
            headline=self._headline,
            description=self._description,
            duration=self._duration,
            type=self._type,
            difficulty=self._difficulty,
            slides=self._slides,
            repository=self._repository,
        )
        _talk.save()
        for _speaker in self._speakers:
            _talk.speakers.add(_speaker)
        for _topic in self._topics:
            _talk.topics.add(_topic)

        return _talk
