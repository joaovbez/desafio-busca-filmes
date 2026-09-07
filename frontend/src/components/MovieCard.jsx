export function MovieCard({ movie }) {
  const year = movie.release_year > 0 ? movie.release_year : null
  const rating =
    typeof movie.vote_average === 'number'
      ? movie.vote_average.toFixed(1)
      : '—'

  return (
    <article className="movie-card">
      <header className="movie-card__header">
        <h2 className="movie-card__title">{movie.title || 'Sem título'}</h2>
        <span className="movie-card__rating" title="Nota média">
          {rating}
        </span>
      </header>
      {year ? <p className="movie-card__year">{year}</p> : null}
      {movie.genres?.length ? (
        <ul className="movie-card__genres">
          {movie.genres.map((genre) => (
            <li key={genre}>{genre}</li>
          ))}
        </ul>
      ) : null}
      {movie.overview ? (
        <p className="movie-card__overview">{movie.overview}</p>
      ) : null}
    </article>
  )
}
