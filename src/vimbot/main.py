import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from vimbot.database import (
    initialize_database,
)
from vimbot.dependencies import get_templates
from vimbot.routers import feedback, queries, root, index_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


templates = get_templates()
folder = os.path.dirname(__file__)

app.mount("/static", StaticFiles(directory=folder + "/../static"), name="static")
app.mount(
    "/templates", StaticFiles(directory=folder + "/../templates"), name="templates"
)

app.include_router(root.router)
app.include_router(queries.router)
# app.include_router(index_api.router)
app.include_router(feedback.router)
