import os
import sqlite_utils
from vimbot.config import settings

# Configuration
idx_root: str = settings.INDEX_ROOT
embedding_model_name: str = settings.EMBEDDING_MODEL.split("/")[-1]
idx_name: str = settings.INDEX_NAME
folder_path: str = f"{idx_root}/{embedding_model_name}_{idx_name}/"
db_path: str = settings.DB_FILE_EMBEDDINGS

# Create or connect to the SQLite database
db: sqlite_utils.Database = sqlite_utils.Database(db_path)


def write_files_from_db(destination_folder: str) -> None:
    """
    Writes files from the SQLite database to the specified destination folder.

    Args:
        destination_folder (str): The root folder where files should be written.
    """

    print("")

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate over the records in the database
    for record in db[embedding_model_name].rows:
        file_path: str = os.path.join(destination_folder, record["filename"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the file content to disk
        with open(file_path, "wb") as file:
            file.write(record["content"])
            print(f"Wrote file {record["filename"]} to disk.")

    print("")
    print(f"Files have been extracted from {db_path} to {folder_path}.")


if __name__ == "__main__":
    write_files_from_db(folder_path)
