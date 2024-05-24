from vimbot.bot.utils.docs_pipeline.get_docs import get_docs
from vimbot.bot.utils.docs_pipeline.docs_to_sqlite import insert_markdown_files
from vimbot.bot.utils.docs_pipeline.make_embeddings import make_embeddings
from vimbot.bot.utils.docs_pipeline.embeddings_to_sqlite import save_files_to_db

# from vimbot.bot.utils.docs_pipeline.sqlite_to_embedding_files import write_files_from_db


def _from_url_to_embeddings():
    """
    Pipeline to retrieve docs from a Git repository,
    insert them into a SQLite database,
    and create embeddings, which are also saved to a SQLite database.
    If restoring from a SQLite database, use write_files_from_db().
    """

    # Step 1: Retrieve docs from the Git repository
    get_docs()

    # Step 2: Insert markdown files into the SQLite database
    insert_markdown_files()

    # Step 3: Create embeddings from the SQLite database
    make_embeddings()

    # Step 4: Write embeddings to a SQLite database
    save_files_to_db()

    # Step 5: Write embeddings from a SQLite database to a directory
    # write_files_from_db()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    _from_url_to_embeddings()
