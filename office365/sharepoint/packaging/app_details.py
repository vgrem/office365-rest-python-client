from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AppDetails(Entity):
    """Specifies the detail properties for a SharePoint Add-in."""

    @odata(name="EulaUrl")
    @property
    def eula_url(self) -> Optional[str]:
        """Specifies the URL to get the End User License Agreement (EULA) information for the SharePoint Add-in."""
        return self.properties.get("EulaUrl", None)

    @odata(name="PrivacyUrl")
    @property
    def privacy_url(self) -> Optional[str]:
        """Specifies the URL of the privacy statement for the SharePoint Add-in."""
        return self.properties.get("PrivacyUrl", None)

    @odata(name="Publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Specifies the publisher name for the SharePoint Add-in."""
        return self.properties.get("Publisher", None)

    @odata(name="ShortDescription")
    @property
    def short_description(self) -> Optional[str]:
        """Specifies a short description for the SharePoint Add-in."""
        return self.properties.get("ShortDescription", None)

    @odata(name="SupportUrl")
    @property
    def support_url(self) -> Optional[str]:
        """Specifies the URL of the support page for the SharePoint Add-in."""
        return self.properties.get("SupportUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Packaging.AppDetails"
