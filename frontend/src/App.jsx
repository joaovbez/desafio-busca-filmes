import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
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
      const response = await fetch(
        `${API_URL}/search?q=${encodeURIComponent(q)}`,
      )
      const data = await response.json()
      if (!response.ok) {
        const detail = data.detail
        const message =
          typeof detail === 'string' ? detail : `Erro ${response.status}`
        throw new Error(message)
      }
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

  return (
    <main className="page">
      <h1>Busca de filmes</h1>
      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="search"
          name="q"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Digite um filme ou uma busca..."
          aria-label="Busca de filmes"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Buscando…' : 'Buscar'}
        </button>
      </form>

      {error ? <p className="status error">{error}</p> : null}
      {loading ? <p className="status">Buscando…</p> : null}
      {result ? (
        <pre className="json">{JSON.stringify(result, null, 2)}</pre>
      ) : null}
    </main>
  )
}

export default App
