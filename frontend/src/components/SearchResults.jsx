import { MovieCard } from './MovieCard.jsx'

export function SearchResults({ result, error, loading }) {
  if (error) {
    return <p className="status error">{error}</p>
  }

  if (loading) {
    return <p className="status">Buscando…</p>
  }

  if (!result) {
    return null
  }

  if (result.results.length === 0) {
    return <p className="status">Nenhum filme encontrado.</p>
  }

  return (
    <section className="results" aria-live="polite">
      <p className="results__count">
        {result.results.length}{' '}
        {result.results.length === 1 ? 'filme' : 'filmes'}
      </p>
      <ul className="results__list">
        {result.results.map((movie) => (
          <li key={movie.id}>
            <MovieCard movie={movie} />
          </li>
        ))}
      </ul>
    </section>
  )
}
