#app/main.py
"""
Application entry point.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.api.v1.router import api_router
from app.db.init_db import init_db



# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events.
    """

    # Startup
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

    yield

    # Shutdown (optional future use)


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
        lifespan=lifespan,  # 🔥 NEW
    )

    # Routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    def root():
        return {"message": f"{settings.PROJECT_NAME} is running"}

    @app.get("/health/db")
    def db_health_check():
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "Database connection OK"}
        except Exception as e:
            return {"status": "Database connection FAILED", "error": str(e)}

    return app


app = create_application()