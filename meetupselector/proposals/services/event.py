from datetime import datetime, time, timedelta

from django.db.models import QuerySet

from ..models import Event


def create(
    name: str,
    description: str,
    meetup_link: str,
    location: str,
    date: datetime,
    start_time: time,
    duration: timedelta,
) -> Event:
    event = Event(
        name=name,
        description=description,
        meetup_link=meetup_link,
        location=location,
        date=date,
        start_time=start_time,
        duration=duration,
    )
    event.save()

    return event


def retrieve_all() -> QuerySet[Event]:
    return Event.objects.all()
