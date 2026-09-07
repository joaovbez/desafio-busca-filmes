export function SearchForm({ query, onQueryChange, loading, onSubmit }) {
  function handleSubmit(event) {
    event.preventDefault()
    onSubmit()
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="search"
        name="q"
        value={query}
        onChange={(event) => onQueryChange(event.target.value)}
        placeholder="Digite um filme ou uma busca..."
        aria-label="Busca de filmes"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Buscando…' : 'Buscar'}
      </button>
    </form>
  )
}
