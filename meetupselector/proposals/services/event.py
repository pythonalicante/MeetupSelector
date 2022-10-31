from ..models import Event


def create(
    name: str,
    description: str,
    meetup_link: str,
    location: str,
    done: bool,
) -> Event:
    event = Event(
        name=name,
        description=description,
        meetup_link=meetup_link,
        location=location,
        done=done,
    )
    event.save()

    return event
