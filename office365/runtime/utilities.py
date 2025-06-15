import mimetypes
from email.message import Message
from urllib.parse import parse_qs, urlparse


def message_to_bytes(message: Message) -> bytes:
    """Convert Message object to bytes representation.

    Args:
        message: Email message to convert

    Returns:
        Bytes representation of the message
    """
    return message.as_bytes()


def is_string(value) -> bool:
    """Check if value is a string type"""
    return isinstance(value, str)


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
