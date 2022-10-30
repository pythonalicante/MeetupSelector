from ninja import ModelSchema

from meetupselector.talks.models import Topic


class TopicListSchema(ModelSchema):
    class Config:
        model = Topic
        model_fields = ["id", "name", "description"]


class TopicRetrieveSchema(ModelSchema):
    class Config:
        model = Topic
        model_fields = ["id", "name", "description", "created_at", "updated_at"]
