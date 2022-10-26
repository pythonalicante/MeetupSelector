from ninja import ModelSchema

from meetupselector.talks.models import Talk, Topic


class TopicRetrieveSchema(ModelSchema):
    class Config:
        model = Topic
        model_fields = ["id", "name", "description", "created_at", "updated_at"]


class TalkListSchema(ModelSchema):
    class Config:
        model = Talk
        model_fields = ["id", "name", "type", "created_at", "updated_at"]
