from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from vimbot.dependencies import get_templates

router = APIRouter()
templates = get_templates()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
