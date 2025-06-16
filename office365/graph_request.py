from __future__ import annotations

from typing import Callable, Dict, Optional

from office365.azure_env import AzureEnvironment
from office365.runtime.auth.entra.authentication_context import AuthenticationContext
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v4.json_format import V4JsonFormat


class GraphRequest(ODataRequest):
    """Microsoft Graph API request handler with authentication support."""

    def __init__(
        self,
        version: str = "v1.0",
        tenant: str = None,
        environment: str = AzureEnvironment.Global,
    ):
        """
        Initialize a Microsoft Graph API request handler.

        Args:
            version: API version (default: "v1.0")
            tenant: Tenant ID or domain name
            environment: Azure environment (default: AzureEnvironment.Global)
        """
        super().__init__(V4JsonFormat())
        self._version = version
        self._environment = environment
        self._auth_context = AuthenticationContext(
            environment=environment, tenant=tenant
        )
        self.beforeExecute += self.authenticate_request

    def with_access_token(
        self, token_callback: Callable[[], Dict[str, str]]
    ) -> GraphRequest:
        """
        Initialize with a token callback function.

        Args:
            token_callback: Function that returns an access token dictionary

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_access_token(token_callback)
        return self

    def with_certificate(
        self, client_id: str, thumbprint: str, private_key: str
    ) -> GraphRequest:
        """
        Initialize with client certificate authentication.

        Args:
            client_id: The OAuth client ID of the calling application
            thumbprint: Certificate thumbprint
            private_key: Private key content

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_certificate(client_id, thumbprint, private_key)
        return self

    def with_client_secret(self, client_id: str, client_secret: str) -> GraphRequest:
        """
        Initialize with client secret authentication.

        Args:
            client_id: The OAuth client ID of the calling application
            client_secret: Client secret value

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_client_secret(client_id, client_secret)
        return self

    def with_token_interactive(
        self, client_id: str, username: Optional[str] = None
    ) -> GraphRequest:
        """
        Initialize with interactive authentication flow.

        Note: Only works if your app is registered with redirect_uri as http://localhost

        Args:
            client_id: The OAuth client ID of the calling application
            username: Typically a UPN in email format (optional)

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_token_interactive(client_id, username)
        return self

    def with_username_and_password(
        self, client_id: str, username: str, password: str
    ) -> GraphRequest:
        """
        Initialize with username/password authentication.

        Args:
            client_id: The OAuth client ID of the calling application
            username: Typically a UPN in email format
            password: User password

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_username_and_password(client_id, username, password)
        return self

    def authenticate_request(self, request: RequestOptions) -> None:
        """
        Authenticate the request by adding a bearer token.

        Args:
            request: The request to authenticate
        """
        token = self._auth_context.acquire_token()
        request.ensure_header("Authorization", "Bearer {0}".format(token.accessToken))

    @property
    def service_root_url(self) -> str:
        """Get the Microsoft Graph service root URL."""
        return "{0}/{1}".format(
            AzureEnvironment.get_graph_authority(self._environment), self._version
        )
