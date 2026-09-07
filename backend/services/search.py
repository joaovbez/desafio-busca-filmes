from models import EMPTY_RANKING, SearchResponse
from services.catalog import MOVIES
from services.parser import parse_query


def search_movies(q: str, limit: int) -> SearchResponse:
    return SearchResponse(
        query=q,
        parsed=parse_query(q),
        ranking=EMPTY_RANKING,
        results=MOVIES[:limit],
    )
