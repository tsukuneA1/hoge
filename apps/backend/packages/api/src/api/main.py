from fastapi import FastAPI
from libs.logging import configure_logging

from logging import getLogger

logger = getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend API",
        version="0.1.0",
    )

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


def main() -> None:
    configure_logging()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
