import './App.css'
import { SearchForm } from './components/SearchForm.jsx'
import { SearchResults } from './components/SearchResults.jsx'
import { useMovieSearch } from './hooks/useMovieSearch.js'

function App() {
  const { query, setQuery, result, error, loading, search } = useMovieSearch()

  return (
    <main className="page">
      <h1>Busca de filmes</h1>
      <SearchForm
        query={query}
        onQueryChange={setQuery}
        loading={loading}
        onSubmit={search}
      />
      <SearchResults result={result} error={error} loading={loading} />
    </main>
  )
}

export default App
