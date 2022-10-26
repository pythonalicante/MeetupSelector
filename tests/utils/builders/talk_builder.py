from datetime import timedelta
from typing import Iterable

from meetupselector.talks.models import Speaker, Talk, Topic


class TalkBuilder:

    _name: str = "name"
    _headline: str = "headline"
    _description: str = "description"
    _duration: timedelta = timedelta(minutes=60)
    _type: str = "T"
    _difficulty: str = "E"
    _speakers: Iterable[Speaker] = []
    _topics: Iterable[Topic] = []

    def with_name(self, name: str) -> "TalkBuilder":
        self._name = name
        return self

    def with_description(self, description: str) -> "TalkBuilder":
        self._description = description
        return self

    def with_headline(self, headline: str) -> "TalkBuilder":
        self._headline = headline
        return self

    def with_duration(self, duration: timedelta) -> "TalkBuilder":
        self._duration = duration
        return self

    def with_type(self, type: str) -> "TalkBuilder":
        self._type = type
        return self

    def with_difficulty(self, difficulty: str) -> "TalkBuilder":
        self._difficulty = difficulty
        return self

    def with_speakers(self, speakers: Iterable[Speaker]) -> "TalkBuilder":
        self._speakers = speakers
        return self

    def with_topics(self, topics: Iterable[Topic]) -> "TalkBuilder":
        self._topics = topics
        return self

    def build(self) -> Talk:
        return Talk.objects.create(
            name=self._name,
            headline=self._headline,
            description=self._description,
            duration=self._duration,
            type=self._type,
            difficulty=self._difficulty,
        )
