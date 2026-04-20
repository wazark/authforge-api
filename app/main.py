# app/main.py
"""
Application entry point.

Initializes FastAPI, registers routes,
and runs startup tasks (like DB seeding).
"""

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.api.v1.router import api_router
from app.db.init_db import init_db


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
    )


    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)


    # Root endpoint
    @app.get("/")
    def root():
        return {"message": f"{settings.PROJECT_NAME} is running"}


    # Database health check
    @app.get("/health/db")
    def db_health_check():
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "Database connection OK"}
        except Exception as e:
            return {"status": "Database connection FAILED", "error": str(e)}


    # Startup event (IMPORTANT)
    @app.on_event("startup")
    def startup_event():
        """
        Runs when the application starts.

        Used to initialize default data (e.g., roles).
        """
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()

    return app



# App instance
app = create_application()