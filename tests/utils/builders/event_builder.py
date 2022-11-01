from meetupselector.proposals.models import Event


class EventBuilder:
    _name: str = "name"
    _description: str = "description"
    _meetup_link: str = "meetup_link"
    _location: str = "location"

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

    def build(self) -> Event:
        return Event.objects.create(
            name=self._name,
            description=self._description,
            meetup_link=self._meetup_link,
            location=self._location,
        )
