import logging
from typing import Optional

from office365.runtime.auth.authentication_provider import AuthenticationProvider
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions

logger = logging.getLogger(__name__)


class NtlmProvider(AuthenticationProvider):
    """
    Provides NTLM authentication for SharePoint On-Premises.

    Note: Due to Outlook REST API v1.0 BasicAuth Deprecation
    (refer https://developer.microsoft.com/en-us/office/blogs/outlook-rest-api-v1-0-basicauth-deprecation/)
    this should not be used for Outlook REST API v1.0.

    Args:
        credentials (UserCredential): User credentials for NTLM authentication
        verify_ssl (bool): Whether to verify SSL certificates (default: True)
        timeout (int): Request timeout in seconds (default: 10)
    """

    def __init__(self, credentials: UserCredential, verify_ssl: bool = True, timeout: int = 10):
        """
        Provides NTLM authentication (intended for SharePoint On-Premises)

        Note: due to Outlook REST API v1.0 BasicAuth Deprecation
        (refer https://developer.microsoft.com/en-us/office/blogs/outlook-rest-api-v1-0-basicauth-deprecation/)
        NetworkCredentialContext class should be no longer utilized for Outlook REST API v1.0

        """
        super().__init__()
        self._last_error: Optional[Exception] = None
        try:
            from requests_ntlm import HttpNtlmAuth

            self.auth = HttpNtlmAuth(credentials.userName, credentials.password)
        except ImportError as e:
            logger.error("Failed to import requests_ntlm package")
            raise ImportError(
                "To use NTLM authentication the package 'requests_ntlm' needs to be installed. "
                "Install it with: pip install requests_ntlm"
            ) from e

        self.verify_ssl = verify_ssl
        self.timeout = timeout
        logger.info("NTLM authentication provider initialized")

    def authenticate_request(self, request: RequestOptions) -> None:
        """
        Authenticates the given request with NTLM.

        Args:
            request (RequestOptions): The request to authenticate

        Raises:
            RuntimeError: If authentication configuration fails
        """

        if not request:
            raise ValueError("Request cannot be None")

        request.auth = self.auth
        request.verify = self.verify_ssl
        request.timeout = self.timeout
        logger.debug("Successfully authenticated request with NTLM")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"verify_ssl={self.verify_ssl}, " f"timeout={self.timeout})"
