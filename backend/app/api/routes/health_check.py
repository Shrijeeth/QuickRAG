from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def root():
    return {
        "success": True,
        "app": "Quick RAG",
        "message": "Server is up and running",
    }
