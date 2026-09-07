from models import MovieResult, ParsedQuery, RankingInfo, SearchResponse
from services.catalog import MOVIES
from services.fusion import reciprocal_rank_fusion
from services.lexical import find_anchor, rank_lexical
from services.parser import parse_query
from services.semantic import rank_semantic, rank_similar


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
    used_semantic = False
    used_rrf = False
    results = candidates

    if parsed.intent == "similar_to" and parsed.anchor:
        anchor = find_anchor(parsed.anchor)
        if anchor is None:
            results = []
        else:
            results = rank_similar(anchor, candidates)
            used_semantic = bool(results)
    elif parsed.free_text:
        lexical_ranked, used_lexical = rank_lexical(candidates, parsed.free_text)
        semantic_ranked, used_semantic = rank_semantic(
            candidates,
            parsed.free_text,
        )
        if used_lexical and used_semantic:
            results = reciprocal_rank_fusion(lexical_ranked, semantic_ranked)
            used_rrf = True
        elif used_lexical:
            results = lexical_ranked
        elif used_semantic:
            results = semantic_ranked

    return SearchResponse(
        query=q,
        parsed=parsed,
        ranking=RankingInfo(
            used_lexical=used_lexical,
            used_semantic=used_semantic,
            used_rrf=used_rrf,
        ),
        results=results[:limit],
    )
