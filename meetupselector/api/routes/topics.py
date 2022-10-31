import typing as t

from ninja import Router
from pydantic import UUID4

from meetupselector.api.schemas.talks import TopicListSchema, TopicRetrieveSchema
from meetupselector.talks.services import TopicService

router = Router()


@router.get("/", response=t.List[TopicListSchema], url_name="list_topics")
def get_topics(_):
    return TopicService.list()


@router.get("/{topic_id}", response=TopicRetrieveSchema, url_name="get_topic")
def get_topic(_, topic_id: UUID4):
    return TopicService.retrieve(topic_id=topic_id)
