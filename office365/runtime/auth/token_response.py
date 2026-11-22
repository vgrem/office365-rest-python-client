from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Optional


class TokenResponse:
    """Represents an OAuth 2.0 token response with Bearer token support.

    Handles parsing and validation of OAuth token responses, including:
    - Access tokens
    - Token types
    - Additional token metadata
    """

    #: The claims this class reads. Declared here because :meth:`from_json` also
    #: carries the rest of the response through ``**kwargs``: a reader of one of
    #: these three is typed, and anything else stays whatever the provider sent.
    accessToken: Optional[str] = None
    tokenType: Optional[str] = None
    expiresIn: Optional[int | str] = None

    def __init__(self, access_token: Optional[str] = None, token_type: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize a token response.

        Args:
            access_token: The OAuth access token string
            token_type: The token type (e.g., "Bearer")
            **kwargs: Additional token response fields
        """
        self.accessToken = access_token
        self.tokenType = token_type
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def is_valid(self) -> bool:
        """Check if the token response contains a valid Bearer token.

        Returns:
            True if accessToken exists and tokenType is "Bearer"
        """
        return self.accessToken is not None and self.tokenType == "Bearer"

    @property
    def authorization_header(self) -> str:
        """Generate an HTTP Authorization header value.

        The scheme is the one the provider reported, which is ``Bearer`` for every
        Microsoft identity platform response and the legacy ``BPOSIDCRL`` for a
        SharePoint app-only one. Returns:
            Formatted "{scheme} {token}" string
        """
        return f"{self.tokenType or 'Bearer'} {self.accessToken}"

    @staticmethod
    def from_json(value: "TokenResponse | Dict[str, Any] | None") -> "TokenResponse":
        """Create a TokenResponse from JSON data.

        Args:
            value: Dictionary containing token response data, or a response that
                was already parsed (returned as it is, so a caller does not have
                to know which a token callback produced)

        Returns:
            New TokenResponse instance

        Raises:
            ValueError: If the JSON contains an error field
        """
        if value is None:
            return TokenResponse()
        if isinstance(value, TokenResponse):
            return value
        error = value.get("error", None)
        if error:
            raise ValueError(value)

        def _normalize_key(name: str) -> str:
            key_parts = name.split("_")
            MIN_KEY_PARTS = 2
            if len(key_parts) >= MIN_KEY_PARTS:
                names = [n.title() for n in key_parts[1:]]
                return key_parts[0] + "".join(names)
            return name

        json = {_normalize_key(k): v for k, v in value.items()}
        return TokenResponse(**json)


#: What a token callback hands back: the response itself, the JSON it was parsed from, or
#: nothing. A callback may also be a coroutine function, which is the second shape.
TokenCallback = Callable[[], TokenResponse | Dict[str, Any] | None]
AsyncTokenCallback = Callable[[], Awaitable[TokenResponse | Dict[str, Any] | None]]
