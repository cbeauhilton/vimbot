import os
import sqlite_utils  # could use sqlmodel instead, but I have no interest in making this db with anything other than sqlite
from vimbot.config import settings


def insert_markdown_files():
    """
    Inserts markdown files from the specified DOCS_FOLDER into a SQLite database.
    """
    db_path = settings.DB_FILE_DOCS
    table_name = settings.DB_FILE_DOCS_TABLE_NAME
    docs_folder = f"{settings.RESOURCE_FOLDER}{settings.REMOTE_DOCS_FOLDER}"

    print(f"\nSaving files from {docs_folder}\ninto the database at {db_path}...\n")
    print("The old db will be overwritten.\n")

    # Connect to the SQLite database (or create it if it doesn't exist)
    db = sqlite_utils.Database(db_path, recreate=True)
    # "recreate" will delete db on every run if it exists

    # Function to insert markdown files into the database
    i = 0

    def _insert_files(folder_path: str, i: int):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    # Construct the slug
                    relative_path = os.path.relpath(root, folder_path)
                    if relative_path.startswith("docs/"):
                        relative_path = relative_path[5:]
                    slug = f"{relative_path}/{file}".replace("\\", "/").strip("/")
                    if slug.endswith(".md"):
                        slug = slug[:-3]  # Remove the .md extension

                    # Read the content of the file
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Insert the content into the database
                    db[table_name].insert(
                        {"slug": slug, "content": content}, pk="id", replace=True
                    )
                    print(f"Inserted file: {file_path}")
                    i += 1
        return i

    # Insert files from the docs folder
    num_files = _insert_files(docs_folder, i)
    #
    # Check if the number of inserted files matches the table length
    db.enable_counts()
    table_length = db.cached_counts([table_name])[
        table_name
    ]  # cached_counts returns something like {'entries': 294}
    assert (
        num_files == table_length
    ), f"Number of inserted files ({num_files}) does not match the table length ({table_length}). Try deleting {db_path} and running this script again."

    print(
        f"\n{num_files} markdown files inserted into the database {db_path} in the table {table_name}."
    )


if __name__ == "__main__":
    insert_markdown_files()
