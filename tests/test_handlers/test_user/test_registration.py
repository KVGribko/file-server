import pytest
from sqlalchemy import select
from starlette import status

from tests.utils import UserFactory

from app.config import get_settings
from app.db.models import User


class TestRegistration:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return f"{settings.PATH_PREFIX}/user/registration"

    @staticmethod
    def get_correct_registration_data() -> dict:
        user = UserFactory()
        return {
            "username": user.username,
            "password": user.password,
        }

    async def test_not_registered_without_credentials(self, client):
        response = await client.post(url=self.get_url())
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_user_registered_with_correct_credentials(self, client, session):
        user_data = self.get_correct_registration_data()
        response = await client.post(url=self.get_url(), json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        query = select(User).filter(User.username == user_data["username"])
        users_in_base = (await session.scalars(query)).all()
        assert len(users_in_base) == 1

    @pytest.mark.parametrize(
        "password",
        (
            "",
            "           ",
            "1234567",
            "ПарольИзРусскихБукв",
            "password with spaces123E",
            "only_lowercase_characters",
            "ONLY_UPPERCASE_CHARACTERS",
            "password_without_NUMBERS",
            "password_without_STR@NGe_symb0^ls",
        ),
    )
    async def test_not_registered_with_incorrect_password(self, client, password):
        user_data = self.get_correct_registration_data()
        user_data["password"] = password
        response = await client.post(url=self.get_url(), json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_not_registered_duplicate_user(self, client, user_with_auth_token):
        user_data = {
            "username": user_with_auth_token["model"].username,
            "password": user_with_auth_token["password"],
        }
        response = await client.post(url=self.get_url(), json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
