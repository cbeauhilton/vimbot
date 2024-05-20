import os
from sqlmodel import create_engine, Session, select
from .config import DB_FILE
from .models import ChatLog

sqlite_url = f"sqlite:///{DB_FILE}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def initialize_database():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    ChatLog.metadata.create_all(engine)


def save_chat_log(query: str, response: str) -> str:
    with Session(engine) as session:
        chat_log = ChatLog(query=query, response=response)
        session.add(chat_log)
        session.commit()
        session.refresh(chat_log)
    return chat_log.uuid


def get_chat_log(uuid: str):
    with Session(engine) as session:
        statement = select(ChatLog).where(ChatLog.uuid == uuid)
        results = session.exec(statement)
        chat_log = results.one()
        return chat_log


def save_thumbs_feedback(uuid: str, helpful: int):
    with Session(engine) as session:
        statement = select(ChatLog).where(ChatLog.uuid == uuid)
        results = session.exec(statement)
        chat_log = results.one()
        if chat_log:
            chat_log.thumbs_up = helpful
            session.commit()


def save_text_feedback(uuid: str, text: str):
    with Session(engine) as session:
        statement = select(ChatLog).where(ChatLog.uuid == uuid)
        results = session.exec(statement)
        chat_log = results.one()
        if chat_log:
            chat_log.text_feedback = text
            session.commit()
