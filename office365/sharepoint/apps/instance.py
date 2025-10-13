from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class AppInstance(Entity):

    @property
    def app_principal_id(self) -> Optional[str]:
        """Gets the AppPrincipalId property"""
        return self.properties.get("AppPrincipalId", None)

    @property
    def app_web_full_url(self) -> Optional[str]:
        """Gets the AppWebFullUrl property"""
        return self.properties.get("AppWebFullUrl", None)

    @property
    def image_fallback_url(self) -> Optional[str]:
        """Gets the ImageFallbackUrl property"""
        return self.properties.get("ImageFallbackUrl", None)

    @property
    def image_url(self) -> Optional[str]:
        """Gets the ImageUrl property"""
        return self.properties.get("ImageUrl", None)

    @property
    def in_error(self) -> Optional[bool]:
        """Gets the InError property"""
        return self.properties.get("InError", None)

    @property
    def start_page(self) -> Optional[str]:
        """Gets the StartPage property"""
        return self.properties.get("StartPage", None)

    @property
    def package_fingerprint(self) -> Optional[bytes]:
        """Gets the PackageFingerprint property"""
        return self.properties.get("PackageFingerprint", None)

    @property
    def product_id(self) -> Optional[UUID]:
        """Gets the ProductId property"""
        return self.properties.get("ProductId", None)

    @property
    def remote_app_url(self) -> Optional[str]:
        """Gets the RemoteAppUrl property"""
        return self.properties.get("RemoteAppUrl", None)

    @property
    def settings_page_url(self) -> Optional[str]:
        """Gets the SettingsPageUrl property"""
        return self.properties.get("SettingsPageUrl", None)

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def status(self) -> Optional[int]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)
