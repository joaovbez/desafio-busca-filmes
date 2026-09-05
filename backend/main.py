from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Busca de Filmes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


class ParsedQuery(BaseModel):
    intent: str
    genres: list[str]
    year_from: Optional[int]
    year_to: Optional[int]
    min_rating: Optional[float]
    free_text: str
    anchor: Optional[str]


class RankingInfo(BaseModel):
    used_lexical: bool
    used_semantic: bool
    used_rrf: bool


class MovieResult(BaseModel):
    id: int
    title: str
    release_year: int
    genres: list[str]
    vote_average: float
    overview: str
    score: float


class SearchResponse(BaseModel):
    query: str
    parsed: ParsedQuery
    ranking: RankingInfo
    results: list[MovieResult]


STUB_MOVIE = MovieResult(
    id=0,
    title="Filme de teste (stub)",
    release_year=0,
    genres=[],
    vote_average=0.0,
    overview="Não veio do CSV. Este resultado é fixo até a busca real existir.",
    score=0.0,
)

EMPTY_PARSED = ParsedQuery(
    intent="search",
    genres=[],
    year_from=None,
    year_to=None,
    min_rating=None,
    free_text="",
    anchor=None,
)

EMPTY_RANKING = RankingInfo(
    used_lexical=False,
    used_semantic=False,
    used_rrf=False,
)


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(...),
    limit: int = Query(10, ge=1),
) -> SearchResponse:
    if not q.strip():
        raise HTTPException(status_code=400, detail="q não pode ser vazio")

    # `limit` já entra no contrato HTTP; fatiar a lista só quando houver resultados reais.
    _ = limit

    return SearchResponse(
        query=q,
        parsed=EMPTY_PARSED,
        ranking=EMPTY_RANKING,
        results=[STUB_MOVIE],
    )
