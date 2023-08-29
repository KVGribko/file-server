from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits

from factory import Factory, Faker


def generate_strong_password(length: int = 30) -> str:
    alphabet = ascii_lowercase + ascii_uppercase + digits + "_"
    return "".join(choice(alphabet) for _ in range(length))


class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")

    def __repr__(self) -> str:
        return f"User(username='{self.username}', password='{self.password}')"


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker("first_name")
    password = generate_strong_password()
    email = Faker("email")
