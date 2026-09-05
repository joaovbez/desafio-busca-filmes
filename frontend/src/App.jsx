import { useState } from 'react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')

  function handleSubmit(event) {
    event.preventDefault()
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
        <button type="submit">Buscar</button>
      </form>
    </main>
  )
}

export default App
