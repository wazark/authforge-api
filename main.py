"""
Application entry point.

This module initializes the FastAPI app,
loads configuration, and includes routers.
"""

from fastapi import FastAPI
from app.core.config import settings


def create_application() -> FastAPI:
    """
    Application factory function.

    Creates and configures the FastAPI app instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="1.0.0"
    )

    # Future: include routers
    # from app.api.v1.router import api_router
    # app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def root():
        """
        Health check endpoint.
        """
        return {
            "message": f"{settings.PROJECT_NAME} is running"
        }

    return app


# Create app instance
app = create_application()