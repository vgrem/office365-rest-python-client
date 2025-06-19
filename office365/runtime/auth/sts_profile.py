from datetime import datetime, timedelta, timezone

from office365.azure_env import AzureEnvironment, get_login_authority
from office365.runtime.utilities import urlparse


class STSProfile:
    """Security Token Service (STS) configuration profile for SharePoint authentication.

    Example:
        >>> profile = STSProfile("https://contoso.sharepoint.com")
        >>> if profile.is_expired:
        >>>   profile.reset()
    """

    TOKEN_ISSUER: str = "urn:federation:MicrosoftOnline"
    DEFAULT_TOKEN_LIFETIME: timedelta = timedelta(minutes=30)

    def __init__(self, site_url: str, environment: AzureEnvironment = None) -> None:
        """Initialize STS profile.

        Args:
            site_url: SharePoint site URL
            environment: Azure environment (defaults to global)
        """
        self._site_url = site_url
        self._environment = environment
        self._created = datetime.now(tz=timezone.utc)
        self._expires = self._created + self.DEFAULT_TOKEN_LIFETIME

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"site_url='{self._site_url}', "
            f"environment={self._environment}, "
            f"expires={self._expires.isoformat()})"
        )

    def reset(self):
        """Renew the token expiration timeframe."""
        self._created = datetime.now(tz=timezone.utc)
        self._expires = self._created + self.DEFAULT_TOKEN_LIFETIME

    @property
    def tenant(self) -> str:
        """Get tenant name from site URL (e.g., 'contoso.sharepoint.com')."""
        return urlparse(self._site_url).netloc

    @property
    def security_token_service_url(self) -> str:
        """STS endpoint for token requests."""
        return f"{get_login_authority(self._environment)}/extSTS.srf"

    @property
    def signin_page_url(self) -> str:
        """SharePoint sign-in page URL."""
        site_info = urlparse(self._site_url)
        return (
            f"{site_info.scheme}://{site_info.netloc}/_forms/default.aspx?wa=wsignin1.0"
        )

    @property
    def user_realm_service_url(self) -> str:
        """User realm discovery endpoint."""
        return f"{get_login_authority(self._environment)}/GetUserRealm.srf"

    @property
    def token_issuer(self) -> str:
        """Fixed token issuer URI for Microsoft Online."""
        return self.TOKEN_ISSUER

    @property
    def created(self) -> datetime:
        """Associated SharePoint site URL."""
        return self._created

    @property
    def expires(self) -> datetime:
        """Token expiration timestamp."""
        return self._expires

    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.now(tz=timezone.utc) >= self._expires

    @property
    def site_url(self) -> str:
        """Associated SharePoint site URL."""
        return self._site_url
