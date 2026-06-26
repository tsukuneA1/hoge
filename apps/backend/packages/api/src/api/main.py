from contextlib import contextmanager

from fastapi import FastAPI
from libs.logging import configure_logging

from api.api import courses
from api.infrastructure.db.database import close_engine, init_engine


@contextmanager
def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    try:
        init_engine()
    except Exception:
        close_engine()
        raise

    yield

    # shutdown
    close_engine()


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Backend API", version="0.1.0", lifespan=lifespan)

    app.include_router(courses.router)

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
