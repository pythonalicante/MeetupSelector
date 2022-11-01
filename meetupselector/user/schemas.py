import re

from pydantic import BaseModel, EmailStr, validator


class SignInSchema(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_validator(cls, value: str) -> str:
        msg_error = (
            "password requirements: min. length of 8 chars, "
            "one uppercase char, one lowercase char, one digit, "
            "one special char (not letter, not number)"
        )
        patterns = (".{8}", "[A-Z]", "[a-z]", "[0-9]", "[^a-zA-Z0-9]")
        for pattern in patterns:
            if re.search(pattern, value) is None:
                raise ValueError(msg_error)

        return value
