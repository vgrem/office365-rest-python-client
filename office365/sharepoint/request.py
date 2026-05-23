from typing import Callable, List, Optional, Union

from requests import Response
from typing_extensions import Self

from office365.azure_env import AzureEnvironment
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery
from office365.sharepoint.webs.context_web_information import ContextWebInformation


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
        self._ctx_web_info = None
        self.beforeExecute += self._auth_context.authenticate_request  # type: ignore[operator]
        self.beforeExecute += self.ensure_form_digest  # type: ignore[operator]

    def set_service_root(self, url: str) -> None:
        super().set_service_root(url)
        self._auth_context.url = url

    def build_request(self, query: ClientQuery) -> RequestOptions:
        request = super().build_request(query)
        if isinstance(self.json_format, JsonLightFormat):
            if isinstance(query, DeleteEntityQuery):
                request.ensure_header("X-HTTP-Method", "DELETE")
                request.ensure_header("IF-MATCH", "*")
            elif isinstance(query, UpdateEntityQuery):
                request.ensure_header("X-HTTP-Method", "MERGE")
                request.ensure_header("IF-MATCH", "*")
        return request

    def _get_context_web_information(self):
        """Returns a ContextWebInformation object that specifies metadata about the site."""
        request = RequestOptions(f"{self.service_root_url}/contextInfo")
        request.method = HttpMethod.Post
        response = self.execute_request_direct(request)
        json_format = JsonLightFormat()
        json_format.function = "GetContextWebInformation"
        return_value = ContextWebInformation()
        self.map_json(response.json(), return_value, json_format)
        return return_value

    def ensure_form_digest(self, request: RequestOptions) -> None:
        if request.url.endswith("/contextInfo"):
            return
        if not self.context_info.is_valid:
            self._ctx_web_info = self._get_context_web_information()
        assert self._ctx_web_info is not None
        request.set_header("X-RequestDigest", self._ctx_web_info.FormDigestValue)

    @property
    def context_info(self) -> ContextWebInformation:
        """Returns a ContextWebInformation object that specifies metadata about the site."""
        if self._ctx_web_info is None:
            self._ctx_web_info = ContextWebInformation()
        return self._ctx_web_info

    def execute_request(self, path: str) -> Response:
        """
        Execute direct request to SharePoint REST endpoint

        Args:
            path: Relative API path

        Returns:
            HTTP response
        """
        request_url = f"{self.service_root_url}/{path}"
        return self.execute_request_direct(RequestOptions(request_url))

    def with_credentials(self, credentials: Union[UserCredential, ClientCredential]) -> Self:
        """
        Initialize authentication with user or client credentials

        Args:
            credentials: Authentication credentials

        Returns:
            Self: Supports method chaining
        """
        self._auth_context.with_credentials(credentials)
        return self

    def with_cookies(self, cookie_source, ttl_seconds=None):
        # type: (object, object) -> Self
        """
        Initializes authentication using browser-session cookies.

        :param object cookie_source: Callable returning Dict[str, str] or an AuthCookies instance.
        :param object ttl_seconds: Optional max age for cached cookies before reloading from source.
        """
        self._auth_context.with_cookies(cookie_source, ttl_seconds)  # type: ignore[arg-type]
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

    def with_device_flow(self, tenant: str, client_id: str, scopes: Optional[List[str]] = None) -> Self:
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

    def with_interactive(self, tenant: str, client_id: str, scopes: Optional[List[str]] = None) -> Self:
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
