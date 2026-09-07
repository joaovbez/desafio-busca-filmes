import json
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

CSV_PATH = Path(__file__).resolve().parent.parent / "tmdb_5000_movies.csv"


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


def _parse_genres(raw: object) -> list[str]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    try:
        items = json.loads(str(raw))
    except json.JSONDecodeError:
        return []
    if not isinstance(items, list):
        return []
    return [item["name"] for item in items if isinstance(item, dict) and "name" in item]


def _parse_year(raw: object) -> int:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return 0
    text = str(raw).strip()
    if len(text) < 4 or not text[:4].isdigit():
        return 0
    return int(text[:4])


def load_catalog() -> list[MovieResult]:
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"CSV não encontrado em {CSV_PATH}. "
            "Coloque tmdb_5000_movies.csv na raiz do repositório."
        )

    frame = pd.read_csv(
        CSV_PATH,
        usecols=["id", "title", "genres", "overview", "vote_average", "release_date"],
    )
    movies: list[MovieResult] = []
    for row in frame.itertuples(index=False):
        vote = float(row.vote_average) if pd.notna(row.vote_average) else 0.0
        overview = "" if pd.isna(row.overview) else str(row.overview)
        title = "" if pd.isna(row.title) else str(row.title)
        movies.append(
            MovieResult(
                id=int(row.id),
                title=title,
                release_year=_parse_year(row.release_date),
                genres=_parse_genres(row.genres),
                vote_average=vote,
                overview=overview,
                score=vote,
            )
        )
    movies.sort(key=lambda movie: movie.vote_average, reverse=True)
    return movies


MOVIES = load_catalog()
print(f"loaded {len(MOVIES)} movies")

app = FastAPI(title="Busca de Filmes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(...),
    limit: int = Query(10, ge=1, le=25),
) -> SearchResponse:
    if not q.strip():
        raise HTTPException(status_code=400, detail="q não pode ser vazio")

    return SearchResponse(
        query=q,
        parsed=EMPTY_PARSED,
        ranking=EMPTY_RANKING,
        results=MOVIES[:limit],
    )
