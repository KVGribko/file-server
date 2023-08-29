from os import environ

from pytest import fixture

from app.config import get_settings


@fixture
def set_wrong_port_for_postgres():
    settings = get_settings()
    old_port = settings.POSTGRES_PORT
    environ["POSTGRES_PORT"] = str(old_port + 1)
    yield
    environ["POSTGRES_PORT"] = str(old_port)
