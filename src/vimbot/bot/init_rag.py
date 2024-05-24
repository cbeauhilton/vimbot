from ragatouille import RAGPretrainedModel  # type: ignore[attr-defined]
from vimbot.config import settings


# Singleton pattern to avoid loading the model multiple times
class RAGModel:
    model_instance: RAGPretrainedModel = None

    @classmethod
    def get_instance(cls) -> RAGPretrainedModel:
        cls.model_instance = RAGPretrainedModel.from_index(
            index_path=settings.INDEX_FULL_PATH,
        )
        return cls.model_instance


def initialize_rag() -> RAGPretrainedModel:
    return RAGModel.get_instance()
