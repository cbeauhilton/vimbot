from fastapi import Form
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from vimbot.database import save_text_feedback, save_thumbs_feedback

router: APIRouter = APIRouter()


@router.post("/feedback", response_class=HTMLResponse)
async def feedback(
    uuid: str = Form(default=...),
    helpful: int = Form(default=None),
    text: str = Form(default=None),
) -> HTMLResponse:
    if helpful:
        print(f"Thumbs feedback: {helpful}")
        save_thumbs_feedback(uuid, helpful)
        return HTMLResponse(
            """
            <div id="thumbsContainer" class="flex justify-center">
                <button class="bg-black rounded">⭐</button>
            </div>
            """
        )
    elif text:
        print(f"Text feedback: {text}")
        save_text_feedback(uuid, text)
        return HTMLResponse(
            '<p class="text-center text-green-500">Thank you for your feedback!</p>'
        )
    else:
        return HTMLResponse(status_code=400, content="Invalid request")
