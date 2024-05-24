import sqlite_utils
from ragatouille import RAGPretrainedModel
from vimbot.config import settings


def make_embeddings():
    print("Starting embedding creation process...")
    db_file = settings.DB_FILE_DOCS
    table_name = settings.DB_FILE_DOCS_TABLE_NAME
    pretrained_embedding_model = settings.EMBEDDING_MODEL

    print(f"Connecting to the SQLite database: {db_file}")

    db = sqlite_utils.Database(db_file)

    print(f"Loading the RAG pretrained model: {pretrained_embedding_model}")
    rag = RAGPretrainedModel.from_pretrained(
        pretrained_embedding_model, index_root=settings.RAG_DIR_PATH
    )

    print("Retrieving entries from the 'markdown_files' table...")
    entries = list(db[table_name].rows)
    print(f"Retrieved {len(entries)} entries from the database.")

    print("Extracting text content from the entries...")
    entry_texts = [entry["content"] for entry in entries]
    print(f"Extracted {len(entry_texts)} text contents from the entries.")

    print("Extracting entry IDs...")
    entry_ids = [str(entry["id"]) for entry in entries]
    print(f"Extracted {len(entry_ids)} entry IDs.")

    print("Extracting entry metadata (slug)...")
    entry_metadatas = [{"slug": entry["slug"]} for entry in entries]
    print(f"Extracted {len(entry_metadatas)} entry metadata objects.")

    max_document_length = 512
    if pretrained_embedding_model == "colbert-ir/colbertv2.0":
        max_document_length = 512
    if pretrained_embedding_model == "jinaai/jina-colbert-v1-en":
        max_document_length = int(8190 / 4)
        # using the full 8190 for the vimbook dataset needs ~47Gb RAM by calculation,
        # probably closer to 64Gb in practice, so shrink it down here

    print(
        f"Indexing the entries using {pretrained_embedding_model} with a context length of {max_document_length}..."
    )
    rag.index(
        collection=entry_texts,
        document_ids=entry_ids,
        document_metadatas=entry_metadatas,
        index_name=f"{pretrained_embedding_model.split('/')[-1]}_{settings.INDEX_NAME}",  # will give e.g. "colbertv2.0_vimbook"
        max_document_length=max_document_length,
        split_documents=True,
        use_faiss=True,
    )
    print("Indexing completed.")

    print("Embedding creation process completed.")


if __name__ == "__main__":
    make_embeddings()
