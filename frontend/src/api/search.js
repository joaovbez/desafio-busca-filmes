const API_URL = 'http://localhost:8000'

export async function searchMovies(q) {
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
  return data
}
