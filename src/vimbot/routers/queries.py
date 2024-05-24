from fastapi import APIRouter, Request

from vimbot.bot.init_rag import initialize_rag
from vimbot.bot.query import process_query  # type: ignore[partially-unknown]
from vimbot.database import (
    get_chat_log,
    save_chat_log,
)
from vimbot.dependencies import get_templates

router: APIRouter = APIRouter()

rags = {}
rags["RAG"] = initialize_rag
templates = get_templates()


@router.post("/query")
async def query(request: Request):
    form_data = await request.form()
    q = form_data.get("query", "")
    uuid = form_data.get("uuid", None)  # Get the UUID from the form data
    model_name = "groq-llama3-70b"
    rag = rags["RAG"]()  # type: ignore[unknown]

    if uuid:
        # Retrieve the previous chat log based on the UUID
        previous_chat_log = get_chat_log(uuid)  # type: ignore[unknown]
        if previous_chat_log:
            # Append the previous query and response to the current query
            q = f"Previous Query: {previous_chat_log.query}\nPrevious Response: {previous_chat_log.response}\nCurrent Query: {q}"

    response = process_query(q, model_name, RAG=rag)  # type: ignore[unknown]
    print("" * 10)
    print(response.strip())
    print("" * 10)

    uuid = save_chat_log(q, response)  # type: ignore[partially-incompatible]

    return templates.TemplateResponse(
        "response.html",
        {"request": request, "response": response, "uuid": uuid},
    )
