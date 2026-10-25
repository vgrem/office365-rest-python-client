from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class Spfx3rdPartyCustomPrincipalInfo(Entity):
    @odata(name="AppId")
    @property
    def app_id(self) -> Optional[str]:
        """Gets the AppId property"""
        return self.properties.get("AppId", None)

    @odata(name="AppUri")
    @property
    def app_uri(self) -> Optional[str]:
        """Gets the AppUri property"""
        return self.properties.get("AppUri", None)

    @odata(name="ClientSecret")
    @property
    def client_secret(self) -> Optional[str]:
        """Gets the ClientSecret property"""
        return self.properties.get("ClientSecret", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ClientSideComponent.Spfx3rdPartyCustomPrincipalInfo"
