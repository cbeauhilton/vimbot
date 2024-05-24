from sqlalchemy.exc import NoResultFound
import pytest
import uuid

# from vimbot.config import settings
from vimbot.database import (
    # initialize_database,
    save_chat_log,
    get_chat_log,
    save_thumbs_feedback,
    save_text_feedback,
)


# def test_initialize_database(tmpdir: pytest.TempPathFactory):
#     if settings.DB_BACKEND == "sqlite":
#         db_file_logs = str(tmpdir.join("test.db"))
#         initialize_database(db_file_logs)
#         assert os.path.exists(db_file_logs)
#     else:
#         # Skip this test if DB_BACKEND is not "sqlite"
#         pass


def test_save_chat_log():
    query = "What is the meaning of life?"
    response = "42"
    chat_log_uuid = save_chat_log(query, response)
    assert isinstance(chat_log_uuid, str)
    assert len(chat_log_uuid) == 36  # UUID length


def test_get_chat_log():
    query = "What is the capital of France?"
    response = "Paris"
    chat_log_uuid = save_chat_log(query, response)
    chat_log = get_chat_log(chat_log_uuid)
    assert chat_log.query == query
    assert chat_log.response == response


def test_get_chat_log_nonexistent():
    nonexistent_uuid = str(uuid.uuid4())
    with pytest.raises(NoResultFound):
        _ = get_chat_log(nonexistent_uuid)


def test_save_thumbs_feedback():
    query = "What is the largest continent?"
    response = "Asia"
    chat_log_uuid = save_chat_log(query, response)
    save_thumbs_feedback(chat_log_uuid, 1)
    chat_log = get_chat_log(chat_log_uuid)
    assert chat_log.thumbs_up == 1


def test_save_thumbs_feedback_nonexistent():
    nonexistent_uuid = str(uuid.uuid4())
    with pytest.raises(NoResultFound):
        save_thumbs_feedback(nonexistent_uuid, 1)


def test_save_text_feedback():
    query = "What is the tallest mountain in the world?"
    response = "Mount Everest"
    chat_log_uuid = save_chat_log(query, response)
    feedback_text = "Great answer!"
    save_text_feedback(chat_log_uuid, feedback_text)
    chat_log = get_chat_log(chat_log_uuid)
    assert chat_log.text_feedback == feedback_text


def test_save_text_feedback_nonexistent():
    nonexistent_uuid = str(uuid.uuid4())
    feedback_text = "This is a test feedback"
    with pytest.raises(NoResultFound):
        save_text_feedback(nonexistent_uuid, feedback_text)
