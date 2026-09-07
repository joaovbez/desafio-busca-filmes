from typing import Optional

from pydantic import BaseModel


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
