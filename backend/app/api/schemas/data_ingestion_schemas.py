# pylint: disable=no-else-return

from enum import Enum

from pydantic import BaseModel


class EmbeddingProviders(Enum):
    OLLAMA = "OLLAMA"
    OPENAI = "OPENAI"

    @staticmethod
    def from_str(provider_name: str):
        provider_name = provider_name.upper()
        if provider_name == "OLLAMA":
            return EmbeddingProviders.OLLAMA
        elif provider_name == "OPENAI":
            return EmbeddingProviders.OPENAI
        raise ValueError("Invalid Embedding Provider")


class UploadAndGenerateEmbeddingsParams(BaseModel):
    provider: EmbeddingProviders
    embedding_model_name: str
    embedding_args: dict | None = None
