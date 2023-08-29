from sqlalchemy import select
from starlette import status

from app.config import get_settings
from app.db.models import User


class TestTakeOut:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return f"{settings.PATH_PREFIX}/user/takeout"

    async def test_not_authenticated(self, client):
        response = await client.delete(url=self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_authenticated(self, client, user_with_auth_token, session):
        response = await client.delete(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_204_NO_CONTENT

        query = select(User).filter(User.username == user_with_auth_token["model"].username)
        users_in_base = (await session.scalars(query)).all()
        assert len(users_in_base) == 0

        response = await client.delete(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
