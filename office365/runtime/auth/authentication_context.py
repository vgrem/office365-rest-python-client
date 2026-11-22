from __future__ import annotations

import asyncio
import inspect
import json
import sys
import threading
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Union, cast

from typing_extensions import Self

from office365.azure_env import AzureEnvironment, get_login_authority
from office365.runtime.auth.certificate import CertificateData, build_client_credential
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.cookies import AuthCookies
from office365.runtime.auth.providers.acs_token_provider import ACSTokenProvider
from office365.runtime.auth.providers.cookie_provider import CookieAuthProvider
from office365.runtime.auth.providers.saml_token_provider import SamlTokenProvider
from office365.runtime.auth.token_response import (
    AsyncTokenCallback,
    TokenCallback,
    TokenResponse,
)
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.deprecated import deprecated
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.http.url import get_absolute_url

if TYPE_CHECKING:
    import msal


class AuthenticationContext:
    """Authentication context for SharePoint OnPremise/SharePoint Online/OneDrive For Business"""

    def __init__(
        self,
        url: str,
        environment: AzureEnvironment = AzureEnvironment.Global,
        allow_ntlm: bool = False,
        browser_mode: bool = False,
        authority: str | None = None,
    ):
        """
        Initialize authentication context

        Args:
            url: SharePoint absolute web or site URL
            environment: Office 365 Cloud Environment endpoint (default: AzureEnvironment.Global)
            allow_ntlm: Whether NTLM authentication is enabled (default: False)
            browser_mode: Enable browser authentication (default: False)
            authority: Override the MSAL authority URL, e.g. for Entra External ID (CIAM):
                https://<tenant>.ciamlogin.com
        """
        self.url = url.rstrip("/")
        self._authenticate: Callable[[RequestOptions], None] | None = None
        self._cached_token = None
        self._environment = environment
        self._lock = threading.RLock()
        self._allow_ntlm = allow_ntlm
        self._browser_mode = browser_mode
        self._token_expires = datetime.max.replace(tzinfo=timezone.utc)
        self._authority = authority
        self._token_func: TokenCallback | None = None
        self._async_token_func: AsyncTokenCallback | None = None
        self._async_lock: asyncio.Lock | None = None
        self._async_lock_loop: asyncio.AbstractEventLoop | None = None

    def _get_authority_url(self, tenant: str) -> str:
        """MSAL authority URL, overridable for Entra External ID (CIAM) tenants."""
        if self._authority is not None:
            return self._authority
        return f"{get_login_authority(self._environment)}/{tenant}"

    def with_authority(self, authority: str) -> Self:
        """Override the MSAL authority URL, e.g. for Entra External ID (CIAM) tenants:

            https://<tenant>.ciamlogin.com

        Args:
            authority: Full authority URL used by all subsequent token acquisitions
        """
        self._authority = authority
        return self

    def with_client_secret(
        self,
        tenant: str,
        client_id: str,
        client_secret: str,
        scopes: List[str] | None = None,
    ) -> Self:
        """Authenticate using client secret (MSAL app-only).

        Args:
            tenant: Tenant name (e.g., "contoso.onmicrosoft.com")
            client_id: Application client ID
            client_secret: Client secret value
            scopes: Requested permission scopes (optional, defaults to {site_url}/.default)

        Returns:
            Self: Supports method chaining
        """
        if scopes is None:
            resource = get_absolute_url(self.url)
            scopes = [f"{resource}/.default"]

        def _acquire_token():
            authority_url = self._get_authority_url(tenant)
            import msal

            app = msal.ConfidentialClientApplication(
                client_id,
                authority=authority_url,
                client_credential=client_secret,
            )
            result = app.acquire_token_for_client(scopes)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_client_certificate(
        self,
        tenant: str,
        client_id: str,
        thumbprint: str | None = None,
        cert_path: str | None = None,
        private_key: str | None = None,
        scopes: List[str] | None = None,
        passphrase: str | None = None,
        *,
        public_certificate: CertificateData | None = None,
        use_sni: bool = False,
    ) -> Self:
        """
        Authenticate using client certificate

        Args:
            tenant: Tenant name (e.g., "contoso.onmicrosoft.com")
            client_id: Application client ID
            thumbprint: Certificate thumbprint (optional when ``public_certificate`` is given)
            cert_path: Path to PEM encoded private key (optional)
            private_key: PEM encoded private key (optional)
            scopes: Requested permission scopes (optional)
            passphrase: Private key passphrase (optional)
            public_certificate: Certificate (DER/PEM bytes, inline PEM text, or a
                path) used to derive the thumbprint or, with ``use_sni``, for
                subject name/issuer authentication (optional)
            use_sni: Use subject name/issuer authentication (requires the optional
                ``cryptography`` package)

        Returns:
            Self: Supports method chaining
        """
        if scopes is None:
            resource = get_absolute_url(self.url)
            scopes = [f"{resource}/.default"]
        if cert_path is None and private_key is None:
            raise ValueError("Private key is missing. Use either 'cert_path' or 'private_key' to pass the value")
        elif cert_path is not None:
            with open(cert_path, "r", encoding="utf8") as f:
                private_key = f.read()

        def _acquire_token():
            authority_url = self._get_authority_url(tenant)
            credentials = build_client_credential(
                thumbprint=thumbprint,
                private_key=private_key,
                public_certificate=public_certificate,
                passphrase=passphrase,
                use_sni=use_sni,
            )
            import msal

            app = msal.ConfidentialClientApplication(
                client_id,
                authority=authority_url,
                client_credential=credentials,
            )
            result = app.acquire_token_for_client(scopes)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_interactive(self, tenant: str, client_id: str, scopes: List[str] | None = None) -> Self:
        """
        Authenticate interactively via browser

        Args:
            tenant: Tenant name
            client_id: Application client ID
            scopes: Requested permission scopes (optional)

        Returns:
            Self: Supports method chaining
        """
        if scopes is None:
            resource = get_absolute_url(self.url)
            scopes = [f"{resource}/.default"]

        def _acquire_token():
            import msal

            app = msal.PublicClientApplication(
                client_id,
                authority=self._get_authority_url(tenant),
                client_credential=None,
            )
            result = app.acquire_token_interactive(scopes=scopes)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_device_flow(
        self,
        tenant: str,
        client_id: str,
        scopes: List[str] | None = None,
        token_cache: "msal.SerializableTokenCache | None" = None,
    ) -> Self:
        """
        Authenticate using device flow

        Args:
            tenant: Tenant name
            client_id: Application client ID
            scopes: Requested permission scopes (optional)
            token_cache: Cache to read and write, so a later session renews the refresh token
                the cache already holds instead of asking for a new device code

        Returns:
            Self: Supports method chaining
        """
        if scopes is None:
            resource = get_absolute_url(self.url)
            scopes = [f"{resource}/.default"]

        def _acquire_token():
            import msal

            app = msal.PublicClientApplication(
                client_id,
                authority=self._get_authority_url(tenant),
                client_credential=None,
                token_cache=token_cache,
            )
            # A cache that already holds this account answers without a code: only a cache with
            # nothing to renew reaches the prompt below, which is what makes a login cheap.
            accounts = app.get_accounts()
            if accounts:
                renewed = app.acquire_token_silent(scopes, account=accounts[0])
                if renewed:
                    return TokenResponse.from_json(renewed)

            flow = app.initiate_device_flow(scopes=scopes)
            if "user_code" not in flow:
                raise ValueError(f"Failed to create device flow: {json.dumps(flow, indent=4)}")

            print(flow["message"])
            sys.stdout.flush()

            result = app.acquire_token_by_device_flow(flow)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_access_token(self, token_func: TokenCallback) -> Self:
        """
        Initialize with token callback function

        Args:
            token_func: Function that returns a token response. It may be a
                regular function or an ``async def`` coroutine function; the
                latter is only supported on the async API.

        Returns:
            Self: Supports method chaining
        """
        # The two shapes cannot be told apart by annotation, only by the object, so the
        # context keeps the one it was handed and the branch is where the cast is due.
        if inspect.iscoroutinefunction(token_func):
            self._async_token_func = cast(AsyncTokenCallback, token_func)
        else:
            self._token_func = token_func

        def _authenticate(request: RequestOptions) -> None:
            token = self._current_token(datetime.now(timezone.utc))
            request.set_header("Authorization", token.authorization_header)

        self._authenticate = _authenticate
        return self

    def _current_token(self, request_time: datetime) -> TokenResponse:
        """The token to authenticate with: the cached one, renewed at most once if due.

        The lock is taken only when a renewal is due, and the expiry is re-checked inside
        it because two threads can arrive holding the same expired token.
        """
        if self._cached_token is not None and request_time <= self._token_expires:
            return self._cached_token
        if self._token_func is None:
            raise RuntimeError(
                "An async token callback requires the async API; await "
                "execute_query_async() / execute_batch_async() instead."
            )
        with self._lock:
            if self._cached_token is None or request_time > self._token_expires:
                return self._apply_token_response(self._token_func(), request_time)
            return self._cached_token

    def _apply_token_response(
        self, token_res: TokenResponse | Dict[str, Any] | None, request_time: datetime
    ) -> TokenResponse:
        """Cache a freshly acquired token, update its expiry, and hand it back."""
        token = TokenResponse.from_json(token_res)
        self._cached_token = token

        if token.expiresIn is not None:
            self._token_expires = request_time + timedelta(seconds=int(token.expiresIn))
        return token

    @property
    def is_async_token_callback(self) -> bool:
        """Whether the currently configured auth hook is an async token callback."""
        return self._async_token_func is not None

    @property
    def access_token(self) -> str | None:
        """The access token this context holds, or ``None`` when it can hold none.

        Acquired on first read and cached, so the answer does not depend on whether a request
        happened to run first; an expired token is returned as it is, because a caller reads it
        for what it *proves* - the audience it was issued for, the permissions it carries - and
        an expiry changes none of that. It is never validated. A cookie-authenticated context
        has no bearer token to show, and answers ``None``.
        """
        if self._cached_token is None and self._token_func is not None:
            with self._lock:
                if self._cached_token is None:
                    self._apply_token_response(self._token_func(), datetime.now(timezone.utc))
        token = self._cached_token
        return None if token is None else getattr(token, "accessToken", None)

    def _get_async_lock(self) -> asyncio.Lock:
        """Return a lock for the running loop, recreating it when the loop changes.

        A lock binds to the loop that first waits on it, so a lock kept across
        two ``asyncio.run()`` calls can fail with ``Event loop is closed`` (or
        hang) once it is contended. The lock exists only to collapse concurrent
        acquisitions, so replacing it for a new loop costs nothing.
        """
        loop = asyncio.get_running_loop()
        if self._async_lock is None or self._async_lock_loop is not loop:
            self._async_lock = asyncio.Lock()
            self._async_lock_loop = loop
        return self._async_lock

    async def acquire_token_async(self) -> TokenResponse | None:
        """Ensure a fresh cached token using the async callback.

        Only meaningful when the token callback is a coroutine function; for any
        other provider this is a no-op returning ``self._cached_token``. Concurrent
        awaiters share one refresh under an :class:`asyncio.Lock`.
        """
        if self._async_token_func is None:
            return self._cached_token
        request_time = datetime.now(timezone.utc)
        if self._cached_token is None or request_time > self._token_expires:
            async with self._get_async_lock():
                if self._cached_token is None or request_time > self._token_expires:
                    self._apply_token_response(await self._async_token_func(), request_time)
        return self._cached_token

    async def authenticate_request_async(self, request: RequestOptions) -> None:
        """Authenticate ``request`` on the event loop via the async token callback."""
        token = await self.acquire_token_async()
        if token is not None:
            request.set_header("Authorization", token.authorization_header)

    def with_cookies(
        self,
        cookie_source: Callable[[], Dict[str, str]] | AuthCookies,
        ttl_seconds: int | None = None,
    ) -> Self:
        """Initializes authentication using browser-session cookies.

        Args:
            cookie_source: Callable returning Dict[str, str] or an AuthCookies instance.
            ttl_seconds: Optional max age for cached cookies before reloading from source.
        """
        provider = CookieAuthProvider(cookie_source, ttl_seconds)
        self._install(provider.authenticate_request)
        return self

    def with_username_and_password(
        self,
        tenant: str,
        client_id: str,
        username: str,
        password: str,
        scopes: List[str] | None = None,
    ) -> Self:
        """Initializes Username and password authentication flow

        Args:
            scopes:
            tenant (str):
            client_id (str): The OAuth client id of the calling application.
            username (str): Typically a UPN in the form of an email address.
            password (str): The password.
        """
        import msal

        authority_url = self._get_authority_url(tenant)

        app = msal.PublicClientApplication(
            authority=authority_url,
            client_id=client_id,
        )

        def _acquire_token():
            result = None
            accounts = app.get_accounts(username=username)
            if accounts:
                result = app.acquire_token_silent(scopes, account=accounts[0])

            if not result:
                token_json = app.acquire_token_by_username_password(
                    username=username,
                    password=password,
                    scopes=scopes,
                )
                result = TokenResponse.from_json(token_json)
            return result

        return self.with_access_token(_acquire_token)

    def with_credentials(self, credentials: Union[UserCredential, ClientCredential]) -> Self:
        """
        Initialize authentication with user or client credentials

        Args:
            credentials: Authentication credentials

        Returns:
            Self: Supports method chaining
        """
        if isinstance(credentials, ClientCredential):
            provider = ACSTokenProvider(
                self.url,
                credentials,
                self._environment,
            )
        elif isinstance(credentials, UserCredential):
            if self._allow_ntlm:
                from office365.runtime.auth.providers.ntlm_provider import NtlmProvider

                provider = NtlmProvider(credentials)
            else:
                raise RuntimeError(
                    "with_user_credentials uses the legacy SAML/ACS auth flow which "
                    "Microsoft has retired for SharePoint Online. "
                    "Use with_username_and_password(tenant, client_id, username, password) instead. "
                    "For on-premises SharePoint, use allow_ntlm=True."
                )
        else:
            raise ValueError("Unknown credential type")

        self._install(provider.authenticate_request)
        return self

    @deprecated(
        reason="Use with_credentials(UserCredential(username, password)) instead",
        version="3.0",
    )
    def acquire_token_for_user(self, username: str, password: str) -> Self:
        """Initializes a client to acquire a token via user credentials

        Args:
            password (str): The user password
            username (str): Typically a UPN in the form of an email address
        """
        provider = SamlTokenProvider(self.url, UserCredential(username, password), self._browser_mode)
        self._install(provider.authenticate_request)
        return self

    def acquire_token_for_app(self, client_id: str, client_secret: str) -> Self:
        """Initializes a client to acquire a token via client credentials (SharePoint App-Only)

        Args:
            client_id (str): The OAuth client id of the calling application.
            client_secret (str): Secret string that the application uses to prove its identity when requesting a token
        """
        provider = ACSTokenProvider(self.url, ClientCredential(client_id, client_secret))
        self._install(provider.authenticate_request)
        return self

    def _install(self, authenticate: Callable[[RequestOptions], None]) -> None:
        """Make ``authenticate`` the one hook every request passes through.

        A context has one way in at a time: a provider installed after a token callback
        replaces it, so the callback is forgotten here - otherwise
        :attr:`is_async_token_callback` would describe a callback nothing calls.
        """
        self._authenticate = authenticate
        self._token_func = None
        self._async_token_func = None

    @property
    def is_configured(self) -> bool:
        """Whether an authentication provider has been set on this context."""
        return self._authenticate is not None

    def authenticate_request(self, request: RequestOptions) -> None:
        """Authenticate the HTTP request

        Args:
            request: The request to authenticate

        Raises:
            ValueError: If authentication credentials are missing or invalid
        """
        if self._authenticate is None:
            raise ValueError("Authentication credentials are missing or invalid")

        self._authenticate(request)
