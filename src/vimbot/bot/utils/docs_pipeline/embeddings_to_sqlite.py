import os
import sqlite_utils
from vimbot.config import settings

# Configuration
idx_root: str = settings.INDEX_ROOT
embedding_model_name: str = settings.EMBEDDING_MODEL.split("/")[-1]
idx_name: str = settings.INDEX_NAME
folder_path: str = f"{idx_root}/{embedding_model_name}_{idx_name}/"
db_path: str = settings.DB_FILE_EMBEDDINGS

# Create the SQLite database
db: sqlite_utils.Database = sqlite_utils.Database(db_path, recreate=True)


def save_files_to_db(
    current_folder: str = folder_path, relative_path: str = ""
) -> None:
    """
    Recursively saves files from the specified folder to the SQLite database.

    Args:
        current_folder (str): The current folder path being processed.
        relative_path (str): The relative path of the current folder from the root folder.
    """
    for filename in os.listdir(current_folder):
        file_path: str = os.path.join(current_folder, filename)
        rel_file_path: str = os.path.join(relative_path, filename)

        # Skip directories and recurse into them
        if os.path.isdir(file_path):
            save_files_to_db(file_path, rel_file_path)
        else:
            # Read the file content and insert it into the database
            with open(file_path, "rb") as file:
                content: bytes = file.read()
            db[embedding_model_name].insert(
                {"filename": rel_file_path, "content": content}, pk="id"
            )
            print(f"Saved {rel_file_path} to the database.")

    print("")
    print(f"\nFiles have been saved to {db_path}.")


if __name__ == "__main__":
    save_files_to_db()
