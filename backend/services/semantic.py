import numpy as np

from helpers import BACKEND_DIR
from models import MovieResult
from services.catalog import MOVIES

CACHE_PATH = BACKEND_DIR / "data" / "embeddings.npz"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_model = None
_vectors: np.ndarray | None = None
_INDEX_BY_ID = {movie.id: idx for idx, movie in enumerate(MOVIES)}


def _movie_text(movie: MovieResult) -> str:
    return f"{movie.title}. {movie.overview}".strip()


def _ensure_index() -> None:
    global _model, _vectors
    if _vectors is not None:
        return

    from sentence_transformers import SentenceTransformer

    ids = np.array([movie.id for movie in MOVIES], dtype=np.int64)
    if CACHE_PATH.is_file():
        cached = np.load(CACHE_PATH)
        if np.array_equal(cached["ids"], ids):
            _vectors = cached["vectors"]
            _model = SentenceTransformer(MODEL_NAME)
            print(f"loaded embeddings from {CACHE_PATH}")
            return

    print("computing movie embeddings (first run)…")
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _model = SentenceTransformer(MODEL_NAME)
    texts = [_movie_text(movie) for movie in MOVIES]
    _vectors = _model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    np.savez(CACHE_PATH, vectors=_vectors, ids=ids)
    print(f"saved embeddings to {CACHE_PATH}")


def rank_semantic(
    movies: list[MovieResult],
    text: str,
) -> tuple[list[MovieResult], bool]:
    if not text.strip() or not movies:
        return movies, False

    _ensure_index()
    assert _model is not None and _vectors is not None
    query = _model.encode(text, normalize_embeddings=True)
    scored: list[tuple[float, MovieResult]] = []
    for movie in movies:
        idx = _INDEX_BY_ID.get(movie.id)
        if idx is None:
            continue
        scored.append((float(_vectors[idx] @ query), movie))

    if not scored:
        return movies, False

    scored.sort(key=lambda item: item[0], reverse=True)
    ranked = [
        movie.model_copy(update={"score": score}) for score, movie in scored
    ]
    return ranked, True


def rank_similar(
    anchor: MovieResult,
    movies: list[MovieResult],
) -> list[MovieResult]:
    _ensure_index()
    assert _vectors is not None
    anchor_idx = _INDEX_BY_ID.get(anchor.id)
    if anchor_idx is None:
        return []

    vector = _vectors[anchor_idx]
    scored: list[tuple[float, MovieResult]] = []
    for movie in movies:
        if movie.id == anchor.id:
            continue
        idx = _INDEX_BY_ID.get(movie.id)
        if idx is None:
            continue
        scored.append((float(_vectors[idx] @ vector), movie))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [movie.model_copy(update={"score": score}) for score, movie in scored]
