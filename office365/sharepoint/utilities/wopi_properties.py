from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class WopiProperties(Entity):
    """Do not use. For internal use only."""

    @odata(name="AccessToken")
    @property
    def access_token(self) -> Optional[str]:
        """Gets the AccessToken property"""
        return self.properties.get("AccessToken", None)

    @odata(name="AccessTokenTtl")
    @property
    def access_token_ttl(self) -> Optional[int]:
        """Gets the AccessTokenTtl property"""
        return self.properties.get("AccessTokenTtl", None)

    @odata(name="AppIconUrl")
    @property
    def app_icon_url(self) -> Optional[str]:
        """Gets the AppIconUrl property"""
        return self.properties.get("AppIconUrl", None)

    @odata(name="ErrorMessageToDisplay")
    @property
    def error_message_to_display(self) -> Optional[str]:
        """Gets the ErrorMessageToDisplay property"""
        return self.properties.get("ErrorMessageToDisplay", None)

    @odata(name="RedirectUrl")
    @property
    def redirect_url(self) -> Optional[str]:
        """Gets the RedirectUrl property"""
        return self.properties.get("RedirectUrl", None)

    @odata(name="WebApplicationUrl")
    @property
    def web_application_url(self) -> Optional[str]:
        """Gets the WebApplicationUrl property"""
        return self.properties.get("WebApplicationUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Utilities.WopiProperties"
