from typing import Literal, Optional

from pydantic import BaseModel, Field


class ParsedQuery(BaseModel):
    intent: Literal["search", "similar_to"] = Field(
        description=(
            "similar_to se a pessoa pede filmes parecidos com um título conhecido; "
            "caso contrário search"
        )
    )
    genres: list[str] = Field(
        description=(
            "Gêneros no vocabulário TMDB em inglês "
            "(Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, "
            "Family, Fantasy, Foreign, History, Horror, Music, Mystery, Romance, "
            "Science Fiction, TV Movie, Thriller, War, Western). "
            "Lista vazia se a query não restringe gênero."
        )
    )
    year_from: Optional[int] = Field(
        default=None,
        description="Ano inicial (inclusivo). Anos 80 → 1980. Sem período → null.",
    )
    year_to: Optional[int] = Field(
        default=None,
        description="Ano final (inclusivo). Anos 80 → 1989. Sem período → null.",
    )
    min_rating: Optional[float] = Field(
        default=None,
        description="Nota mínima (0–10) se a pessoa pediu rating/nota acima de X.",
    )
    free_text: str = Field(
        description=(
            "Texto livre que não virou filtro: título, tema da sinopse, etc. "
            "Vazio se a query for só filtro ou só similar_to."
        )
    )
    anchor: Optional[str] = Field(
        default=None,
        description="Título do filme âncora quando intent é similar_to.",
    )


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
