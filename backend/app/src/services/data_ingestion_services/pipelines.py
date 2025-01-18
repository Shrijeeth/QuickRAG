from haystack import Pipeline

from app.src.services.data_ingestion_services.components import (
    pdf_converter,
    document_cleaner,
    document_splitter,
    qdrant_writer,
)
from app.src.services.data_ingestion_services.helpers import get_document_embedder


def build_and_save_pdf_document_pipeline(build_params: dict) -> Pipeline:
    document_embedder = get_document_embedder(
        build_params["provider"], build_params["embedder_args"]
    )

    pipeline = Pipeline(
        metadata={
            "pipeline_id": build_params["credential_id"],
        }
    )

    pipeline.add_component("converter", pdf_converter)
    pipeline.add_component("document_cleaner", document_cleaner)
    pipeline.add_component("document_splitter", document_splitter)
    pipeline.add_component("document_embedder", document_embedder)
    pipeline.add_component("document_writer", qdrant_writer)

    pipeline.connect("converter", "document_cleaner")
    pipeline.connect("document_cleaner", "document_splitter")
    pipeline.connect("document_splitter", "document_embedder")
    pipeline.connect("document_embedder", "document_writer")

    with open(
        f"{build_params['credential_id']}_data_ingestion_pipeline.yaml",
        "w",
        encoding="utf-8",
    ) as f:
        pipeline.dump(f)

    return pipeline
