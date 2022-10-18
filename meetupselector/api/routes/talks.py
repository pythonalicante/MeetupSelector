import typing as t

from ninja import Router
from pydantic import UUID4

from meetupselector.api.schemas.talks import TopicListSchema, TopicRetrieveSchema
from meetupselector.talks.services import TopicService

router = Router()


@router.get("/topic", response=t.List[TopicListSchema], url_name="list_topics")
def get_topics(_):
    return TopicService.list()


@router.get("/topic/{topic_id}", url_name="get_topic", response=TopicRetrieveSchema)
def get_topic(_, topic_id: UUID4):
    return TopicService.get(topic_id=topic_id)
