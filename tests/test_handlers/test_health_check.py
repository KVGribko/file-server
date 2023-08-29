from starlette import status

from app.config import get_settings


class TestHealthCheckHandler:
    @staticmethod
    def get_url(with_database: bool = False) -> str:
        settings = get_settings()
        if with_database:
            return f"{settings.PATH_PREFIX}/health_check/ping_database"
        return f"{settings.PATH_PREFIX}/health_check/ping"

    async def test_ping(self, client):
        response = await client.get(url=self.get_url())
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_database(self, client):
        response = await client.get(self.get_url(with_database=True))
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_database_with_error(self, client, set_wrong_port_for_postgres):
        response = await client.get(self.get_url(with_database=True))
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
