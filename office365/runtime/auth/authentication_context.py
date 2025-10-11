from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, List, Union

from typing_extensions import Self

from office365.azure_env import AzureEnvironment, get_login_authority
from office365.runtime.auth.client_credential import ClientCredential
from office365.runtime.auth.providers.acs_token_provider import ACSTokenProvider
from office365.runtime.auth.providers.saml_token_provider import SamlTokenProvider
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.utilities import deprecated, get_absolute_url


def _get_authorization_header(token: Any) -> str:
    return f"{token.tokenType} {token.accessToken}"


class AuthenticationContext:
    """Authentication context for SharePoint OnPremise/SharePoint Online/OneDrive For Business"""

    def __init__(
        self,
        url: str,
        environment: AzureEnvironment = None,
        allow_ntlm: bool = False,
        browser_mode: bool = False,
    ):
        """
        Initialize authentication context

        Args:
            url: SharePoint absolute web or site URL
            environment: Office 365 Cloud Environment endpoint (default: AzureEnvironment.Global)
            allow_ntlm: Whether NTLM authentication is enabled (default: False)
            browser_mode: Enable browser authentication (default: False)
        """
        self.url = url.rstrip("/")
        self._authenticate = None
        self._cached_token = None
        self._environment = environment
        self._allow_ntlm = allow_ntlm
        self._browser_mode = browser_mode
        self._token_expires = datetime.max.replace(tzinfo=timezone.utc)

    def with_client_certificate(
        self,
        tenant: str,
        client_id: str,
        thumbprint: str,
        cert_path: str = None,
        private_key: str = None,
        scopes: List[str] = None,
        passphrase: str = None,
    ):
        """
        Authenticate using client certificate

        Args:
            tenant: Tenant name (e.g., "contoso.onmicrosoft.com")
            client_id: Application client ID
            thumbprint: Certificate thumbprint
            cert_path: Path to PEM encoded certificate (optional)
            private_key: PEM encoded private key (optional)
            scopes: Requested permission scopes (optional)
            passphrase: Private key passphrase (optional)

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
            authority_url = f"{get_login_authority(self._environment)}/{tenant}"
            credentials = {
                "thumbprint": thumbprint,
                "private_key": private_key,
                "passphrase": passphrase,
            }
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

    def with_interactive(self, tenant: str, client_id: str, scopes: List[str] = None) -> Self:
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
                authority=f"{get_login_authority(self._environment)}/{tenant}",
                client_credential=None,
            )
            result = app.acquire_token_interactive(scopes=scopes)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_device_flow(self, tenant: str, client_id: str, scopes: List[str] = None):
        """
        Authenticate using device flow

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
                authority=f"{get_login_authority(self._environment)}/{tenant}",
                client_credential=None,
            )

            flow = app.initiate_device_flow(scopes=scopes)
            if "user_code" not in flow:
                raise ValueError("Failed to create device flow: %s" % json.dumps(flow, indent=4))

            print(flow["message"])
            sys.stdout.flush()

            result = app.acquire_token_by_device_flow(flow)
            return TokenResponse.from_json(result)

        self.with_access_token(_acquire_token)
        return self

    def with_access_token(self, token_func: Callable[[], TokenResponse]) -> Self:
        """
        Initialize with token callback function

        Args:
            token_func: Function that returns a token response

        Returns:
            Self: Supports method chaining
        """

        def _authenticate(request: RequestOptions) -> Self:

            request_time = datetime.now(timezone.utc)

            if self._cached_token is None or request_time > self._token_expires:
                self._cached_token = token_func()
                if hasattr(self._cached_token, "expiresIn"):
                    self._token_expires = request_time + timedelta(seconds=self._cached_token.expiresIn)
            request.set_header("Authorization", _get_authorization_header(self._cached_token))

        self._authenticate = _authenticate
        return self

    def with_username_and_password(
        self,
        tenant: str,
        client_id: str,
        username: str,
        password: str,
        scopes: List[str] = None,
    ) -> Self:
        """
        Initializes Username and password authentication flow

        :param scopes:
        :param str tenant:
        :param str client_id: The OAuth client id of the calling application.
        :param str username: Typically a UPN in the form of an email address.
        :param str password: The password.
        """
        import msal

        authority_url = f"{get_login_authority(self._environment)}/{tenant}"

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

    def with_credentials(self, credentials: Union[UserCredential, ClientCredential]) -> AuthenticationContext:
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

                import warnings

                warnings.warn(
                    "Use with_username_and_password instead. Microsoft 365 solutions we will be "
                    "retiring the use of Azure ACS (Access Control Services) for SharePoint Online auth.",
                    DeprecationWarning,
                    stacklevel=2,
                )

                provider = SamlTokenProvider(
                    self.url,
                    credentials,
                    self._browser_mode,
                    self._environment,
                )
        else:
            raise ValueError("Unknown credential type")

        self._authenticate = provider.authenticate_request
        return self

    @deprecated(
        reason="Use with_credentials(UserCredential(username, password)) instead",
        version="3.0",
    )
    def acquire_token_for_user(self, username: str, password: str) -> Self:
        """
        Initializes a client to acquire a token via user credentials

        :param str password: The user password
        :param str username: Typically a UPN in the form of an email address
        """
        provider = SamlTokenProvider(self.url, UserCredential(username, password), self._browser_mode)
        self._authenticate = provider.authenticate_request
        return self

    def acquire_token_for_app(self, client_id, client_secret) -> Self:
        """
        Initializes a client to acquire a token via client credentials (SharePoint App-Only)

        :param str client_id: The OAuth client id of the calling application.
        :param str client_secret: Secret string that the application uses to prove its identity when requesting a token
        """
        provider = ACSTokenProvider(self.url, ClientCredential(client_id, client_secret))
        self._authenticate = provider.authenticate_request
        return self

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
