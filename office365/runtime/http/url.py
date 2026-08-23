from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def is_absolute_url(url: str) -> bool:
    """Determine if a URL is absolute (contains network location)."""
    return bool(urlparse(url).netloc)


def get_absolute_url(url: str) -> str:
    """Extract the base URL (scheme+netloc) from a full URL.

    Example:
        >>> get_absolute_url("https://example.com/path?query=1")
        'https://example.com'
    """
    path = urlparse(url).path
    return url.replace(path, "")


def parse_query_param(url: str, key: str) -> str:
    """Extract the first value of a query string parameter.

    Args:
        url: URL containing query string
        key: Query parameter key to look up

    Returns:
        First value for the specified key

    Raises:
        KeyError: If parameter not found
    """
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)[key][0]
