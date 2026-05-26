import requests

# In-memory cache to remember verified IDs during runtime
_artwork_cache = set()

def validate_artwork_id(artwork_id: int) -> bool:
    """
    Queries the Art Institute of Chicago API to check if an artwork ID exists.
    Returns True if valid, False otherwise.
    """
    if artwork_id in _artwork_cache:
        return True

    url = f"https://api.artic.edu/api/v1/artworks/{artwork_id}"
    try:
        # 5-second timeout prevents our server from hanging if their API is slow
        response = requests.get(url, timeout=5.0)
        if response.status_code == 200:
            _artwork_cache.add(artwork_id)
            return True
        return False
    except requests.RequestException:
        return False