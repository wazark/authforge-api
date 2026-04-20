# app/main.py
"""
Application entry point.

This module initializes the FastAPI app,
loads configuration, and includes routers.
"""

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
    )

    @app.get("/")
    def root():
        return {"message": f"{settings.PROJECT_NAME} is running"}

    @app.get("/health/db")
    def db_health_check():
        """
        Checks database connectivity.
        """
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "Database connection OK"}
        except Exception as e:
            return {"status": "Database connection FAILED", "error": str(e)}

    return app


app = create_application()