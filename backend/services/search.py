from models import EMPTY_PARSED, EMPTY_RANKING, SearchResponse
from services.catalog import MOVIES


def search_movies(q: str, limit: int) -> SearchResponse:
    return SearchResponse(
        query=q,
        parsed=EMPTY_PARSED,
        ranking=EMPTY_RANKING,
        results=MOVIES[:limit],
    )
