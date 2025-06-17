import json
from typing import Dict, Optional


class AuthCookies:
    """Handles authentication cookies for SharePoint Online authentication.

    Provides properties and methods to validate, serialize, and deserialize
    SharePoint auth cookies including FedAuth, SPOIDCRL, and rtFa tokens.
    """

    def __init__(self, cookies: Dict[str, str]) -> None:
        """Initialize with authentication cookies.

        Args:
            cookies: Dictionary containing authentication cookies
        """
        self._cookies = cookies

    @property
    def is_valid(self) -> bool:
        """Validates whether the cookies contain required authentication tokens.

        Returns:
            True if cookies contain either FedAuth or SPOIDCRL token, False otherwise
        """
        return bool(self._cookies) and (
            self.fed_auth is not None or self.spo_idcrl is not None
        )

    @property
    def cookie_header(self) -> str:
        """Converts stored cookies into an HTTP Cookie header string.

        Returns:
            Formatted Cookie header string ready for HTTP requests
        """
        return "; ".join(f"{key}={val}" for key, val in self._cookies.items())

    @property
    def fed_auth(self) -> Optional[str]:
        """Gets the primary FedAuth authentication token.

        Returns:
            FedAuth token value if present, None otherwise
        """
        return self._cookies.get("FedAuth", None)

    @property
    def spo_idcrl(self) -> Optional[str]:
        """Gets the secondary SPOIDCRL authentication token (SharePoint Online Identity CRL).

        Returns:
            SPOIDCRL token value if present, None otherwise
        """
        return self._cookies.get("SPOIDCRL", None)

    @property
    def rt_fa(self) -> Optional[str]:
        """Gets the refresh token for Federated Authentication.

        Returns:
            rtFa token value if present, None otherwise
        """
        return self._cookies.get("rtFa", None)

    def to_json(self) -> str:
        """Serializes cookies to JSON format.

        Returns:
            JSON string representation of the cookies
        """
        return json.dumps(self._cookies, indent=2)

    @classmethod
    def from_json(cls, json_data) -> "AuthCookies":
        """Deserializes cookies from JSON format.

        Args:
            json_data: JSON string containing cookie data

        Returns:
            New AuthCookies instance initialized with the deserialized cookies
        """
        cookies_dict = json.loads(json_data)
        return cls(cookies_dict)
