from datetime import datetime

from meetupselector.user.models import User


class UserBuilder:
    _email: str = "topic"
    _description: str = "description"
    _is_staff: bool = False
    _date_joined: datetime = datetime.now()

    def with_email(self, email) -> "UserBuilder":
        self._email = email
        return self

    def with_description(self, description: str) -> "UserBuilder":
        self._description = description
        return self

    def with_is_Staff(self, is_Staff: bool) -> "UserBuilder":
        self._is_Staff = is_Staff
        return self

    def with_date_joined(self, date_joined: datetime) -> "UserBuilder":
        self._date_joined = date_joined
        return self

    def build(self) -> User:
        return User.objects.create(
            email=self._email,
            description=self._description,
            is_staff=self._is_staff,
            date_joined=self._date_joined,
        )
