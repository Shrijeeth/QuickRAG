from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import OpenAIDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
from haystack_integrations.document_stores.qdrant import (
    QdrantDocumentStore,
)


# Data Preprocessing Components
pdf_converter = PyPDFToDocument()
document_cleaner = DocumentCleaner(
    remove_empty_lines=True,
    remove_extra_whitespaces=True,
    unicode_normalization="NFC",
)
document_splitter = DocumentSplitter(
    split_by="passage",
    split_length=5,
    split_overlap=1,
)


# Data Embedding Components
def get_openai_embedder(api_key: str, model: str) -> OpenAIDocumentEmbedder:
    return OpenAIDocumentEmbedder(api_key=api_key, model=model)


def get_ollama_embedder(url: str, model: str) -> OllamaDocumentEmbedder:
    return OllamaDocumentEmbedder(url=url, model=model)


# Vector Store Components
qdrant_document_store = QdrantDocumentStore(
    ":memory:",
    recreate_index=True,
    return_embedding=True,
    wait_result_from_api=True,
)
qdrant_writer = DocumentWriter(
    document_store=qdrant_document_store,
    policy=DuplicatePolicy.SKIP,
)
