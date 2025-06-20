import mimetypes
import warnings
from functools import wraps
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


def get_mime_type(file_name: str) -> tuple[str, str]:
    """Guess the MIME type and encoding for a filename.

    Returns:
        Tuple of (type, encoding) where either may be None
    """
    return mimetypes.guess_type(file_name)


def deprecated(reason: str, version: str = "next"):
    """Mark functions/methods as deprecated with a warning.

    Args:
        reason: Explanation why this is deprecated
        version: Version when this will be removed
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in v{version}. {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
