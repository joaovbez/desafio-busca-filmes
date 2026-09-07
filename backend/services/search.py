from models import MovieResult, ParsedQuery, RankingInfo, SearchResponse
from services.catalog import MOVIES
from services.lexical import rank_lexical
from services.parser import parse_query


def apply_hard_filters(
    movies: list[MovieResult],
    parsed: ParsedQuery,
) -> list[MovieResult]:
    filtered = movies

    if parsed.genres:
        wanted = set(parsed.genres)
        filtered = [
            movie for movie in filtered if wanted.intersection(movie.genres)
        ]

    if parsed.year_from is not None:
        filtered = [
            movie
            for movie in filtered
            if movie.release_year >= parsed.year_from
        ]

    if parsed.year_to is not None:
        filtered = [
            movie
            for movie in filtered
            if 0 < movie.release_year <= parsed.year_to
        ]

    if parsed.min_rating is not None:
        filtered = [
            movie
            for movie in filtered
            if movie.vote_average >= parsed.min_rating
        ]

    return filtered


def search_movies(q: str, limit: int) -> SearchResponse:
    parsed = parse_query(q)
    candidates = apply_hard_filters(MOVIES, parsed)
    
    used_lexical = False
    if parsed.free_text:
        candidates, used_lexical = rank_lexical(candidates, parsed.free_text)
    
    return SearchResponse(
        query=q,
        parsed=parsed,
        ranking=RankingInfo(
            used_lexical=used_lexical,
            used_semantic=False,
            used_rrf=False,
        ),
        results=candidates[:limit],
    )
