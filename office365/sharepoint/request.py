from typing import Callable, List, Optional, Union

from requests import Response
from typing_extensions import Self

from office365.azure_env import AzureEnvironment
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat


class SharePointRequest(ODataRequest):
    """Client request for SharePoint REST API


    Typical usage:
        >>> request = SharePointRequest()
        >>> response = request.execute_request("web/currentUser")
        >>> json = json.loads(response.content)
        >>> prop_val = json["d"]["UserPrincipalName"]
    """

    def __init__(
        self,
        base_url: str,
        environment: AzureEnvironment = AzureEnvironment.Global,
        allow_ntlm: bool = False,
        browser_mode: bool = False,
    ):
        """
        Initialize SharePoint request client

        Args:
            base_url: Absolute Web or Site URL
            environment: Office 365 Cloud Environment endpoint (default: AzureEnvironment.Global)
            allow_ntlm: Whether NTLM authentication is enabled (default: False)
            browser_mode: Enable browser authentication (default: False)
        """
        super().__init__(JsonLightFormat())
        self._auth_context = AuthenticationContext(
            url=base_url,
            environment=environment,
            allow_ntlm=allow_ntlm,
            browser_mode=browser_mode,
        )
        self.beforeExecute += self._auth_context.authenticate_request

    def execute_request(self, path: str) -> Response:
        """
        Execute direct request to SharePoint REST endpoint

        Args:
            path: Relative API path

        Returns:
            HTTP response
        """
        request_url = "{0}/{1}".format(self.service_root_url, path)
        return self.execute_request_direct(RequestOptions(request_url))

    def with_credentials(
        self, credentials: Union[UserCredential, ClientCredential]
    ) -> Self:
        """
        Initialize authentication with user or client credentials

        Args:
            credentials: Authentication credentials

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_credentials(credentials)
        return self

    def with_client_certificate(
        self,
        tenant: str,
        client_id: str,
        thumbprint: str,
        cert_path: Optional[str] = None,
        private_key: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        passphrase: Optional[str] = None,
    ) -> Self:
        """
        Authenticate using client certificate

        Args:
            tenant: Tenant name
            client_id: Application client ID
            thumbprint: Certificate thumbprint
            cert_path: Path to PEM encoded certificate (optional)
            private_key: PEM encoded private key (optional)
            scopes: Requested permission scopes (optional)
            passphrase: Private key passphrase (optional)

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_client_certificate(
            tenant, client_id, thumbprint, cert_path, private_key, scopes, passphrase
        )
        return self

    def with_device_flow(
        self, tenant: str, client_id: str, scopes: Optional[List[str]] = None
    ) -> Self:
        """
        Authenticate using device flow

        Args:
            tenant: Tenant name
            client_id: Application client ID
            scopes: Requested permission scopes (optional)

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_device_flow(tenant, client_id, scopes)
        return self

    def with_interactive(
        self, tenant: str, client_id: str, scopes: Optional[List[str]] = None
    ) -> Self:
        """
        Authenticate interactively via browser

        Args:
            tenant: Tenant name
            client_id: Application client ID
            scopes: Requested permission scopes (optional)

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_interactive(tenant, client_id, scopes)
        return self

    def with_access_token(self, token_func: Callable[[], TokenResponse]) -> Self:
        """
        Initialize with token callback function

        Args:
            token_func: Function that returns a token response

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_access_token(token_func)
        return self

    @property
    def authentication_context(self) -> AuthenticationContext:
        """Get the authentication context"""
        return self._auth_context

    @property
    def base_url(self) -> str:
        """Represents Base Url"""
        return self._auth_context.url

    @property
    def service_root_url(self) -> str:
        """Get the SharePoint REST API service root URL"""
        return f"{self._auth_context.url}/_api"
