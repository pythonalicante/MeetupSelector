from datetime import datetime, time, timedelta

from meetupselector.proposals.models import Event


class EventBuilder:
    _name: str = "name"
    _description: str = "description"
    _meetup_link: str = "https://www.meetup.com/"
    _location: str = "location"
    _date: datetime = datetime.now() + timedelta(days=5)
    _start_time: time = datetime.now().time()
    _duration: timedelta = timedelta(hours=2)  # Future date

    def with_name(self, name: str) -> "EventBuilder":
        self._name = name
        return self

    def with_description(self, description: str) -> "EventBuilder":
        self._description = description
        return self

    def with_meetup_link(self, meetup_link: str) -> "EventBuilder":
        self._meetup_link = meetup_link
        return self

    def with_location(self, location: str) -> "EventBuilder":
        self._location = location
        return self

    def with_date(self, date: datetime) -> "EventBuilder":
        self._date = date
        return self

    def with_start_time(self, start_time: time) -> "EventBuilder":
        self._start_time = start_time
        return self

    def with_duration(self, duration: timedelta) -> "EventBuilder":
        self._duration = duration
        return self

    def build(self) -> Event:
        return Event.objects.create(
            name=self._name,
            description=self._description,
            meetup_link=self._meetup_link,
            location=self._location,
            date=self._date,
            start_time=self._start_time,
            duration=self._duration,
        )
