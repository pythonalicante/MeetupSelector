from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return str(user.is_active) + str(user.pk) + str(timestamp)


token_generator = UserPasswordResetTokenGenerator()
