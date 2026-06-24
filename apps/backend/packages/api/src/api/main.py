from fastapi import FastAPI
from libs.logging import configure_logging

from api.api import courses


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="Backend API",
        version="0.1.0",
    )

    app.include_router(courses.router)

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
