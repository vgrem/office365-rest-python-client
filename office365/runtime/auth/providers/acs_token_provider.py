from typing import Optional

import requests

from office365.azure_env import AzureEnvironment, get_login_authority
from office365.runtime.auth.authentication_provider import AuthenticationProvider
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.utilities import urlparse


class ACSTokenProvider(AuthenticationProvider):
    """Provides OAuth authentication via Azure Access Control Service (ACS)."""

    SHAREPOINT_PRINCIPAL = "00000003-0000-0ff1-ce00-000000000000"

    def __init__(
        self,
        url: str,
        client_id: str,
        client_secret: str,
        environment: AzureEnvironment = None,
    ):
        """Initialize ACS token provider.

        Args:
            url: SharePoint web or site URL
            client_id: OAuth client ID of the calling application
            client_secret: Client secret for proving application identity
            environment: Office 365 Cloud Environment endpoint (defaults to Azure Global)
        """
        self.url = url
        self.redirect_url = None
        self.error = None
        self._client_id = client_id
        self._client_secret = client_secret
        self._cached_token = None  # type: Optional[TokenResponse]
        self._environment = environment

    def authenticate_request(self, request: RequestOptions) -> None:
        """Authenticate the request with an access token."""
        if self._cached_token is None:
            self._cached_token = self.get_app_only_access_token()
        request.set_header("Authorization", self._cached_token.authorization_header)

    def get_app_only_access_token(self) -> TokenResponse:
        """Retrieve an app-only access token from ACS.

        Raises:
            ValueError: If token acquisition fails
        """
        try:
            realm = self._get_realm_from_target_url()
            url_info = urlparse(self.url)
            return self._get_app_only_access_token(url_info.hostname, realm)
        except requests.exceptions.RequestException as e:
            self.error = (
                e.response.text
                if e.response is not None
                else "Acquire app-only access token failed."
            )
            raise ValueError(self.error)

    def _get_app_only_access_token(
        self, target_host: str, target_realm: str
    ) -> TokenResponse:
        """Retrieve app-only access token for target principal.

        Args:
            target_host: URL authority of the target principal
            target_realm: Realm for token's nameid and audience
        """
        resource = self.get_formatted_principal(
            self.SHAREPOINT_PRINCIPAL, target_host, target_realm
        )
        principal_id = self.get_formatted_principal(self._client_id, None, target_realm)
        sts_url = self.get_security_token_service_url(target_realm)
        oauth2_request = {
            "grant_type": "client_credentials",
            "client_id": principal_id,
            "client_secret": self._client_secret,
            "scope": resource,
            "resource": resource,
        }
        response = requests.post(
            url=sts_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=oauth2_request,
        )
        response.raise_for_status()
        return TokenResponse.from_json(response.json())

    def _get_realm_from_target_url(self) -> Optional[str]:
        """Get the realm for the target URL."""
        response = requests.head(url=self.url, headers={"Authorization": "Bearer"})
        header_key = "WWW-Authenticate"
        if header_key in response.headers:
            auth_values = response.headers[header_key].split(",")
            bearer = auth_values[0].split("=")
            return bearer[1].replace('"', "")
        return None

    @staticmethod
    def get_formatted_principal(principal: str, host: Optional[str], realm: str) -> str:
        """Format principal name for token request."""
        return f"{principal}/{host}@{realm}" if host else f"{principal}@{realm}"

    def get_security_token_service_url(self, realm: str) -> str:
        """Get security token service URL."""
        if self._environment:
            base_url = get_login_authority(self._environment)
            return f"{base_url}/{realm}/tokens/OAuth/2"
        return f"https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2"
