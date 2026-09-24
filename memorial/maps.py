from urllib.parse import quote


def google_maps_directions_url(destination: str) -> str:
    """Open Google Maps directions to destination (origin = user's location)."""
    return f"https://www.google.com/maps/dir/?api=1&destination={quote(destination)}"


def google_maps_place_url(destination: str) -> str:
    """Open Google Maps at the destination (map preview, not turn-by-turn)."""
    return f"https://www.google.com/maps/search/?api=1&query={quote(destination)}"
