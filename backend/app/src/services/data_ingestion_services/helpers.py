# pylint: disable=no-else-return

from app.src.services.data_ingestion_services.components import (
    get_openai_embedder,
    get_ollama_embedder,
)


def get_document_embedder(provider: str, embedder_args: dict):
    if provider == "OpenAI":
        return get_openai_embedder(**embedder_args)
    elif provider == "Ollama":
        return get_ollama_embedder(**embedder_args)
    raise ValueError(f"Invalid provider: {provider}")
