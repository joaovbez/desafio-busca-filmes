from fastapi import APIRouter, HTTPException, Query

from models import SearchResponse
from services.search import search_movies

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(...),
    limit: int = Query(10, ge=1, le=25),
) -> SearchResponse:
    if not q.strip():
        raise HTTPException(status_code=400, detail="q não pode ser vazio")
    return search_movies(q, limit)
