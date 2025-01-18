from fastapi import APIRouter, File, Form, UploadFile


router = APIRouter()


@router.post("/upload-and-generate-embeddings")
def upload_and_generate_embeddings(
    file: UploadFile = File(...),
    embedding_model_name: str = Form(...),
    api_key: str = Form(...),
):
    pass
