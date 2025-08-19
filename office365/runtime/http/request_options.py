from dataclasses import dataclass, field
from typing import Any, BinaryIO, Dict, Optional, Union

from office365.runtime.http.http_method import HttpMethod


@dataclass
class RequestOptions:
    """HTTP request configuration

    Attributes:
        url: Target URL for the request
        method: HTTP method (default: GET)
        data: Request payload (bytes, file-like, or dict)
        headers: Request headers
        auth: Authentication handler
        verify: SSL verification flag
        stream: Streaming response flag
        proxies: Proxy configuration
    """

    url: str
    method: HttpMethod = HttpMethod.Get
    data: Optional[Union[str, bytes, BinaryIO, Dict[str, Any]]] = None
    headers: Dict[str, str] = field(default_factory=dict)
    auth: Optional[Any] = None
    verify: bool = True
    stream: bool = False
    proxies: Optional[Dict[str, str]] = None
    timeout: bool = None

    def __str__(self) -> str:
        return f"{self.method} {self.url}"

    @property
    def is_file(self) -> bool:
        """Check if data is a file-like object."""
        return hasattr(self.data, "read") and callable(self.data.read)

    @property
    def is_bytes(self) -> bool:
        """Check if data is bytes-like."""
        return isinstance(self.data, bytes) or (
            hasattr(self.data, "decode") and callable(self.data.decode)
        )

    def set_header(self, name: str, value: Any) -> None:
        """Set a request header."""
        self.headers[name] = str(value)

    def ensure_header(self, name: str, value: Any) -> None:
        """Set header only if it doesn't already exist."""
        self.headers.setdefault(name, str(value))
