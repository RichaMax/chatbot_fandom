from fastapi import FastAPI
from backend.routes.ask import router as ask_router
from backend.routes.history import router as history_router
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ask_router)
    app.include_router(history_router)

    return app
