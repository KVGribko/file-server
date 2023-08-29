from app.endpoints.auth import api_router as auth_router
from app.endpoints.health_check import api_router as health_check_router


list_of_routes = [
    auth_router,
    health_check_router,
]


__all__ = [
    "list_of_routes",
]
