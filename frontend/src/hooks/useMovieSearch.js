import { useState } from 'react'
import { searchMovies } from '../api/search.js'

export function useMovieSearch() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function search() {
    const q = query.trim()
    if (!q) {
      setError('Digite algo para buscar.')
      setResult(null)
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await searchMovies(q)
      setResult(data)
    } catch (err) {
      setError(
        err.message === 'Failed to fetch'
          ? 'Não foi possível falar com a API. Ela está rodando na porta 8000?'
          : err.message,
      )
    } finally {
      setLoading(false)
    }
  }

  return { query, setQuery, result, error, loading, search }
}
