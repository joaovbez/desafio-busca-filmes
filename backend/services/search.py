from models import EMPTY_RANKING, MovieResult, ParsedQuery, SearchResponse
from services.catalog import MOVIES
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
    results = apply_hard_filters(MOVIES, parsed)[:limit]
    return SearchResponse(
        query=q,
        parsed=parsed,
        ranking=EMPTY_RANKING,
        results=results,
    )
