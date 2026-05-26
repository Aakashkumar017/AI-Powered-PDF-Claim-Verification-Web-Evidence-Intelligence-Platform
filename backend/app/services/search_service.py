from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str) -> list[dict]:
    """
    Search the web for evidence related to a claim.
    Returns a list of result dicts with 'content' and 'url' keys.
    Returns an empty list on failure so the caller can still proceed.
    """
    if not query or not query.strip():
        return []

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
        )
        return response.get("results", [])
    except Exception as e:
        print(f"[search_service] search_web error: {e}")
        return []