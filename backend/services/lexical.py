import re

from rank_bm25 import BM25Okapi

from models import MovieResult
from services.catalog import MOVIES

_TOKEN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN.findall(text or "")]


def _document(movie: MovieResult) -> list[str]:
    title = tokenize(movie.title)
    overview = tokenize(movie.overview)
    return title + title + title + overview


_CORPUS = [_document(movie) for movie in MOVIES]
_BM25 = BM25Okapi(_CORPUS)
_INDEX_BY_ID = {movie.id: idx for idx, movie in enumerate(MOVIES)}


def rank_lexical(
    movies: list[MovieResult],
    free_text: str,
) -> tuple[list[MovieResult], bool]:
    tokens = tokenize(free_text)
    if not tokens or not movies:
        return movies, False

    scores = _BM25.get_scores(tokens)
    scored: list[tuple[float, MovieResult]] = []
    for movie in movies:
        idx = _INDEX_BY_ID.get(movie.id)
        if idx is None:
            continue
        scored.append((float(scores[idx]), movie))

    if not scored or max(item[0] for item in scored) <= 0:
        return movies, False

    scored.sort(key=lambda item: item[0], reverse=True)
    ranked = [
        movie.model_copy(update={"score": score}) for score, movie in scored
    ]
    return ranked, True
