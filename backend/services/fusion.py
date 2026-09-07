from models import MovieResult

RRF_K = 60


def reciprocal_rank_fusion(
    lexical: list[MovieResult],
    semantic: list[MovieResult],
) -> list[MovieResult]:
    lex_rank = {movie.id: rank for rank, movie in enumerate(lexical, start=1)}
    sem_rank = {movie.id: rank for rank, movie in enumerate(semantic, start=1)}
    by_id = {movie.id: movie for movie in lexical}
    for movie in semantic:
        by_id.setdefault(movie.id, movie)

    fused: list[tuple[float, MovieResult]] = []
    for movie_id, movie in by_id.items():
        score = 0.0
        if movie_id in lex_rank:
            score += 1.0 / (RRF_K + lex_rank[movie_id])
        if movie_id in sem_rank:
            score += 1.0 / (RRF_K + sem_rank[movie_id])
        fused.append((score, movie))

    fused.sort(key=lambda item: item[0], reverse=True)
    return [movie.model_copy(update={"score": score}) for score, movie in fused]
