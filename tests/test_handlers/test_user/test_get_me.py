from starlette import status

from app.config import get_settings
from app.db.models import User


class TestGetMe:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return f"{settings.PATH_PREFIX}/user/me"

    @staticmethod
    def check_format_of_handler_response(response_body, user: User):
        assert response_body.keys() == {"username", "dt_created", "dt_updated"}
        assert response_body["username"] == user.username

    async def test_success_response_with_header(self, client, user_with_auth_token):
        response = await client.get(url=self.get_url(), headers=user_with_auth_token["header"])
        assert response.status_code == status.HTTP_200_OK
        self.check_format_of_handler_response(response.json(), user_with_auth_token["model"])

    async def test_return_unauthorized_without_header(self, client, user_with_auth_token):
        response = await client.get(url=self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
