from uuid import uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel  # type: ignore[reportOptionalMemberAccess]


class ChatLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    query: str
    response: str
    thumbs_up: int | None = None
    text_feedback: str | None = None
