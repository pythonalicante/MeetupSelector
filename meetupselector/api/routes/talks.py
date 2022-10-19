import logging
import typing as t

from ninja import Router
from pydantic import UUID4

from meetupselector.api.schemas.talks import (
    TalkCreateSchema,
    TalkListSchema,
    TalkRetrieveSchema,
    TopicListSchema,
    TopicRetrieveSchema,
)
from meetupselector.talks.services import TalkService, TopicService

logger = logging.getLogger(__name__)

router = Router()


@router.get("/topic", response=t.List[TopicListSchema], url_name="list_topics")
def get_topics(_):
    return TopicService.list()


@router.get("/topic/{topic_id}", response=TopicRetrieveSchema, url_name="get_topic")
def get_topic(_, topic_id: UUID4):
    return TopicService.get(topic_id=topic_id)


@router.get("/talk", response=t.List[TalkListSchema], url_name="list_talks")
def get_talks(_):
    return TalkService.list()


@router.get("/talk/{talk_id}", response=TalkRetrieveSchema, url_name="get_talk")
def get_talk(_, talk_id: UUID4):
    return TalkService.get(talk_id=talk_id)


@router.post("/talk", response={201: TalkRetrieveSchema})
def create_talk(_, talk: TalkCreateSchema):
    return 201, TalkService.create(**talk.dict())
