from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import (
    initialize_database,
    save_chat_log,
    save_thumbs_feedback,
    save_text_feedback,
)
from .bot.init_rag import initialize_rag
from .bot.query import process_query

rags = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    rags["RAG"] = initialize_rag
    _ = initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/query")
async def query(request: Request):
    form_data = await request.form()
    q = form_data.get("query", "")
    uuid = form_data.get("uuid", None)  # Get the UUID from the form data
    model_name = "groq-llama3-70b"
    rag = rags["RAG"]()

    if uuid:
        # Retrieve the previous chat log based on the UUID
        previous_chat_log = get_chat_log(uuid)
        if previous_chat_log:
            # Append the previous query and response to the current query
            q = f"Previous Query: {previous_chat_log.query}\nPrevious Response: {previous_chat_log.response}\nCurrent Query: {q}"

    response = process_query(q, model_name, RAG=rag)
    print("" * 10)
    print(response.strip())
    print("" * 10)

    uuid = save_chat_log(q, response)

    return templates.TemplateResponse(
        "response.html",
        {"request": request, "response": response, "uuid": uuid},
    )


@app.post("/feedback", response_class=HTMLResponse)
async def feedback(
    uuid: str = Form(...), helpful: int = Form(None), text: str = Form(None)
):
    if helpful is not None:
        print(helpful)
        save_thumbs_feedback(uuid, helpful)
        return HTMLResponse(
            """
            <div id="thumbsContainer" class="flex justify-center">
            <button class="bg-black rounded">⭐</button>
            </div>
            """
        )
    elif text:
        print(text)
        save_text_feedback(uuid, text)
        return HTMLResponse(
            '<p class="text-center text-green-500">Thank you for your feedback!</p>'
        )
    return HTMLResponse(status_code=400, content="Invalid request")
