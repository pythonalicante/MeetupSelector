from ninja import ModelSchema

from meetupselector.user.models import User


class LoginSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["email", "password"]
