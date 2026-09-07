import os

from openai import OpenAI

from models import ParsedQuery

TMDB_GENRES = {
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Family",
    "Fantasy",
    "Foreign",
    "History",
    "Horror",
    "Music",
    "Mystery",
    "Romance",
    "Science Fiction",
    "TV Movie",
    "Thriller",
    "War",
    "Western",
}

SYSTEM_PROMPT = """Você extrai restrições de uma busca de filmes.
Responda só pelo schema. Use gêneros TMDB em inglês da descrição do campo.
Décadas: "anos 80" → year_from 1980 e year_to 1989.
Não invente filtro que a pessoa não pediu.
Tema vago da história (final triste, viagem no espaço) vai em free_text, não em gênero.
"""


def _fallback(q: str) -> ParsedQuery:
    return ParsedQuery(
        intent="search",
        genres=[],
        year_from=None,
        year_to=None,
        min_rating=None,
        free_text=q.strip(),
        anchor=None,
    )


def _sanitize(parsed: ParsedQuery) -> ParsedQuery:
    genres = [genre for genre in parsed.genres if genre in TMDB_GENRES]
    intent = parsed.intent
    anchor = parsed.anchor.strip() if parsed.anchor else None
    if intent == "similar_to" and not anchor:
        intent = "search"
    return parsed.model_copy(
        update={
            "genres": genres,
            "intent": intent,
            "anchor": anchor,
            "free_text": (parsed.free_text or "").strip(),
        }
    )


def parse_query(q: str) -> ParsedQuery:
    if not os.getenv("OPENAI_API_KEY"):
        return _fallback(q)

    try:
        client = OpenAI()
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q},
            ],
            response_format=ParsedQuery,
        )
        parsed = completion.choices[0].message.parsed
        if parsed is None:
            return _fallback(q)
        return _sanitize(parsed)
    except Exception:
        return _fallback(q)
