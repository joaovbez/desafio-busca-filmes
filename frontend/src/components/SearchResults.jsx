export function SearchResults({ result, error, loading }) {
  return (
    <>
      {error ? <p className="status error">{error}</p> : null}
      {loading ? <p className="status">Buscando…</p> : null}
      {result ? (
        <pre className="json">{JSON.stringify(result, null, 2)}</pre>
      ) : null}
    </>
  )
}
