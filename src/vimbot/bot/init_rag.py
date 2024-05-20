from ragatouille import RAGPretrainedModel  # type: ignore[attr-defined]


def initialize_rag():
    RAG = RAGPretrainedModel.from_index(
        "./.ragatouille/colbert/indexes/vimbook-sqlite/"
    )
    return RAG
