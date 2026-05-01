#app/main.py
"""
Application entry point.
"""

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.api.v1.router import api_router
from app.db.init_db import init_db
from app.core.rate_limiter import limiter

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
        lifespan=lifespan,
    )

    # CORS CONFIG (ESSENCIAL PARA FLUTTER WEB)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, restringir
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate Limiter
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # 🚨 Rate limit handler
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
        )

    # Routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Root
    @app.get("/")
    def root():
        return {"message": f"{settings.PROJECT_NAME} is running"}

    # DB Health Check
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