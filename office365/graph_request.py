from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from office365.azure_env import AzureEnvironment, get_graph_authority
from office365.graph_version import GraphVersion
from office365.runtime.auth.certificate import CertificateData
from office365.runtime.auth.entra.authentication_context import AuthenticationContext
from office365.runtime.auth.token_response import TokenCallback
from office365.runtime.http.method import HttpMethod
from office365.runtime.http.prefer import prefer_upsert
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.request import ODataRequest
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.queries.client_query import ClientQuery
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery
from office365.runtime.queries.upsert_entity import UpsertEntityQuery

if TYPE_CHECKING:
    import msal

    from office365.licensing.guard import LicenceGuard


class GraphRequest(ODataRequest):
    """Microsoft Graph API request handler with authentication support."""

    def __init__(
        self,
        version: GraphVersion = GraphVersion.default(),
        tenant: Optional[str] = None,
        environment: AzureEnvironment = AzureEnvironment.Global,
        authority: Optional[str] = None,
        scopes: Optional[List[str]] = None,
        token_cache: "msal.SerializableTokenCache | None" = None,
        licence_guard: Optional[LicenceGuard] = None,
    ):
        """
        Initialize a Microsoft Graph API request handler.

        Args:
            version: API version (default: "v1.0")
            tenant: Tenant ID or domain name
            environment: Azure environment (default: AzureEnvironment.Global)
            authority: Override the MSAL authority URL (e.g. https://<tenant>.ciamlogin.com)
            scopes: Scopes requested to access the API
            token_cache: MSAL token cache to keep the session in
            licence_guard: Asked about a query before it becomes a request, so a call this
                tenant cannot make is refused rather than sent and denied. ``None`` (the
                default) asks nothing; the client passes its own guard in.
        """
        super().__init__("", V4JsonFormat())
        self._version = version
        self._environment = environment
        self._auth_context = AuthenticationContext(
            environment=environment,
            tenant=tenant,
            scopes=scopes,
            token_cache=token_cache,
            authority=authority,
        )
        self.beforeExecute += self.authenticate_request
        self._async_authenticate = self.authenticate_request_async
        self._licence_guard = licence_guard

    def with_access_token(self, token_callback: TokenCallback) -> GraphRequest:
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
        self,
        client_id: str,
        thumbprint: str | None = None,
        private_key: str | None = None,
        *,
        public_certificate: CertificateData | None = None,
        passphrase: str | None = None,
        use_sni: bool = False,
    ) -> GraphRequest:
        """
        Initialize with client certificate authentication.

        Args:
            client_id: The OAuth client ID of the calling application
            thumbprint: Certificate thumbprint (optional when ``public_certificate`` is given)
            private_key: Private key content
            public_certificate: Certificate (DER/PEM bytes, inline PEM text, or a
                path) used to derive the thumbprint or, with ``use_sni``, for
                subject name/issuer authentication
            passphrase: Private key passphrase
            use_sni: Use subject name/issuer authentication (requires the optional
                ``cryptography`` package)

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_certificate(
            client_id,
            thumbprint,
            private_key,
            public_certificate=public_certificate,
            passphrase=passphrase,
            use_sni=use_sni,
        )
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

    def with_token_interactive(self, client_id: str, username: Optional[str] = None) -> GraphRequest:
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

    def with_username_and_password(self, client_id: str, username: str, password: str) -> GraphRequest:
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

    def with_device_flow(self, client_id: str) -> GraphRequest:
        """
        Initialize with device code flow authentication.

        Useful for CLI tools and headless environments. The user authenticates
        by visiting a URL on another device and entering the displayed code.

        Args:
            client_id: The OAuth client ID of the calling application

        Returns:
            self: Supports fluent method chaining
        """
        self._auth_context.with_device_flow(client_id)
        return self

    def authenticate_request(self, request: RequestOptions) -> None:
        """
        Authenticate the request by adding a bearer token.

        Args:
            request: The request to authenticate
        """
        if request.authenticated:
            return  # already authenticated by :meth:`authenticate_request_async`
        token = self._auth_context.acquire_token()
        request.set_header("Authorization", token.authorization_header)

    async def authenticate_request_async(self, request: RequestOptions) -> None:
        """Authenticate the request on the event loop.

        A no-op unless the registered token callback is a coroutine function, in
        which case the token is awaited (single-flight) and the request is
        flagged so the offloaded synchronous auth hook skips it.

        Args:
            request: The request to authenticate
        """
        if not self._auth_context.is_async_token_callback:
            return
        token = await self._auth_context.acquire_token_async()
        request.set_header("Authorization", token.authorization_header)
        request.authenticated = True

    def build_request(self, query: ClientQuery) -> RequestOptions:
        if self._licence_guard is not None:
            # Before anything is built: a refusal here is a call that never reached the service,
            # which is what tells it apart from the 403 an unlicensed tenant would answer with.
            self._licence_guard.check_query(query)
        request = super().build_request(query)
        if isinstance(query, UpsertEntityQuery):
            request.method = HttpMethod.Patch
            prefer_upsert(request)
            if query.if_match is not None:
                request.set_header("If-Match", query.if_match)
            if query.if_none_match is not None:
                request.set_header("If-None-Match", query.if_none_match)
        elif isinstance(query, UpdateEntityQuery):
            request.method = HttpMethod.Patch
        elif isinstance(query, DeleteEntityQuery):
            request.method = HttpMethod.Delete
        return request

    @property
    def service_root_url(self) -> str:
        """Get the Microsoft Graph service root URL."""
        return f"{get_graph_authority(self._environment)}/{self._version.value}"

    @property
    def version(self) -> GraphVersion:
        """Get the current Graph API version."""
        return self._version

    @version.setter
    def version(self, value: GraphVersion) -> None:
        """Set the Graph API version."""
        self._version = value

    @property
    def authentication_context(self) -> AuthenticationContext:
        return self._auth_context
