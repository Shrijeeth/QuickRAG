import json

from fastapi import APIRouter, File, Form, UploadFile

from app.api.schemas.data_ingestion_schemas import (
    UploadAndGenerateEmbeddingsParams,
    EmbeddingProviders,
)


router = APIRouter()


@router.post("/upload-and-generate-embeddings")
def upload_and_generate_embeddings(
    file: UploadFile = File(...),
    provider_name: str = Form(...),
    embedding_model_name: str = Form(...),
    embedding_args: str | None = Form(default=None),
):
    parsed_embedding_args = {}
    if embedding_args:
        try:
            parsed_embedding_args = json.loads(embedding_args)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON provided in embedding_args"}
    params = UploadAndGenerateEmbeddingsParams(
        embedding_model_name=embedding_model_name,
        embedding_args=parsed_embedding_args,
        provider=EmbeddingProviders.from_str(provider_name),
    )
    return params
