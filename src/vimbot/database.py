from sqlmodel import create_engine, Session, select
from sqlalchemy.exc import NoResultFound

from vimbot.config import settings
from vimbot.models import ChatLog

if settings.DB_BACKEND == "sqlite":
    sqlite_url = f"{settings.DB_BACKEND}:///{settings.DB_FILE_LOGS}"
else:
    raise ValueError(f"Unsupported database backend: {settings.DB_BACKEND}")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def initialize_database():
    if settings.DB_BACKEND == "sqlite":
        print("Using sqlite backend.")
    # elif settings.DB_BACKEND == "postgresql":
    #     postgresql_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    #     engine = create_engine(postgresql_url, echo=True)
    else:
        raise ValueError(f"Unsupported database backend: {settings.DB_BACKEND}")

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
        try:
            chat_log = results.one()
            return chat_log
        except NoResultFound:
            raise NoResultFound(f"Chat log with UUID {uuid} not found")


def save_thumbs_feedback(uuid: str, helpful: int):
    with Session(engine) as session:
        try:
            statement = select(ChatLog).where(ChatLog.uuid == uuid)
            results = session.exec(statement)
            chat_log = results.one()
            chat_log.thumbs_up = helpful
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"Chat log with UUID {uuid} not found")


def save_text_feedback(uuid: str, text: str):
    with Session(engine) as session:
        try:
            statement = select(ChatLog).where(ChatLog.uuid == uuid)
            results = session.exec(statement)
            chat_log = results.one()
            chat_log.text_feedback = text
            session.commit()
        except NoResultFound:
            raise NoResultFound(f"Chat log with UUID {uuid} not found")
