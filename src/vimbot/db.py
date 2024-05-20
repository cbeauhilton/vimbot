import os
from typing import TypedDict
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from .config import DB_NAME, DB_BACKEND


class ChatLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    query: str
    model: str
    response: str
    timestamp: str
    feedback_score: int | None = Field(default=None)
    feedback_text: str | None = Field(default=None)
    helpful: bool | None = Field(default=None)
    feedback_text0: str | None = Field(default=None)


class FeedbackDict(TypedDict):
    score: str
    text: str | None


def get_engine():
    if DB_BACKEND == "sqlite":
        return create_engine(f"sqlite:///{DB_NAME}", echo=True)
    else:
        raise NotImplementedError(f"Backend '{DB_BACKEND}' is not yet implemented.")


def initialize_database():
    if not os.path.exists(DB_NAME):
        SQLModel.metadata.create_all(get_engine())


def log_chat(query: str, model: str, response: str) -> int:
    with Session(get_engine()) as session:
        chat_log = ChatLog(
            query=query,
            model=model,
            response=response,
            timestamp=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
        )
        session.add(chat_log)
        session.commit()
        session.refresh(chat_log)
        return chat_log.id


def update_feedback(chat_id: int, helpful: str, feedback_text: str | None = None):
    with Session(get_engine()) as session:
        statement = select(ChatLog).where(ChatLog.id == chat_id)
        results = session.exec(statement)
        chat_log = results.one()
        chat_log.helpful = helpful.lower() == "yes"
        if feedback_text is not None:
            chat_log.feedback_text0 = feedback_text
        session.add(chat_log)
        session.commit()
        return chat_log.id


# def submit_feedback(chat_id: int, feedback: FeedbackDict):
#     with Session(get_engine()) as session:
#         statement = select(ChatLog).where(ChatLog.id == chat_id)
#         results = session.exec(statement)
#         chat_log = results.one()
#         face = feedback["score"]
#         feedback_score = {"😀": 5, "🙂": 4, "😐": 3, "🙁": 2, "😞": 1}[face]
#         feedback_text = feedback["text"] or "none"
#         chat_log.feedback_score = feedback_score
#         chat_log.feedback_text = feedback_text
#         session.add(chat_log)
#         session.commit()
#         return chat_log.id
