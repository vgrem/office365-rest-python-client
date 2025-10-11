from typing import Any, Dict


class TokenResponse:
    """Represents an OAuth 2.0 token response with Bearer token support.

    Handles parsing and validation of OAuth token responses, including:
    - Access tokens
    - Token types
    - Additional token metadata
    """

    def __init__(self, access_token: str = None, token_type: str = None, **kwargs: Any) -> None:
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
    def authorization_header(self):
        """Generate an HTTP Authorization header value.

        Returns:
            Formatted "Bearer {token}" string
        """
        return "Bearer {0}".format(self.accessToken)

    @staticmethod
    def from_json(value: Dict[str, Any]) -> "TokenResponse":
        """Create a TokenResponse from JSON data.

        Args:
            value: Dictionary containing token response data

        Returns:
            New TokenResponse instance

        Raises:
            ValueError: If the JSON contains an error field
        """
        error = value.get("error", None)
        if error:
            raise ValueError(value)

        def _normalize_key(name: str) -> str:
            key_parts = name.split("_")
            if len(key_parts) >= 2:
                names = [n.title() for n in key_parts[1:]]
                return key_parts[0] + "".join(names)
            return name

        json = {_normalize_key(k): v for k, v in value.items()}
        return TokenResponse(**json)
