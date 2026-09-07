function yearLabel(parsed) {
  if (parsed.year_from && parsed.year_to) {
    if (parsed.year_from === parsed.year_to) {
      return String(parsed.year_from)
    }
    return `${parsed.year_from}–${parsed.year_to}`
  }
  if (parsed.year_from) {
    return `a partir de ${parsed.year_from}`
  }
  if (parsed.year_to) {
    return `até ${parsed.year_to}`
  }
  return null
}

export function ParsedInsight({ parsed }) {
  if (!parsed) {
    return null
  }

  const chips = []
  if (parsed.intent === 'similar_to' && parsed.anchor) {
    chips.push(`parecidos com ${parsed.anchor}`)
  }
  for (const genre of parsed.genres ?? []) {
    chips.push(genre)
  }
  const years = yearLabel(parsed)
  if (years) {
    chips.push(years)
  }
  if (parsed.min_rating != null) {
    chips.push(`nota ≥ ${parsed.min_rating}`)
  }
  if (parsed.free_text) {
    chips.push(`texto: ${parsed.free_text}`)
  }

  if (chips.length === 0) {
    return (
      <p className="parsed">
        Não extraímos filtros desta busca. A lista ainda é só por nota.
      </p>
    )
  }

  return (
    <div className="parsed">
      <p className="parsed__label">O que entendemos</p>
      <ul className="parsed__chips">
        {chips.map((chip) => (
          <li key={chip}>{chip}</li>
        ))}
      </ul>
    </div>
  )
}
