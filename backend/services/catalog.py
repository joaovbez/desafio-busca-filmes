import pandas as pd

from helpers import CSV_PATH, parse_genres, parse_year
from models import MovieResult


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
                release_year=parse_year(row.release_date),
                genres=parse_genres(row.genres),
                vote_average=vote,
                overview=overview,
                score=vote,
            )
        )
    movies.sort(key=lambda movie: movie.vote_average, reverse=True)
    return movies


MOVIES = load_catalog()
print(f"loaded {len(MOVIES)} movies")
