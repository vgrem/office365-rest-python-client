from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class App(Entity):
    @odata(name="AssetId")
    @property
    def asset_id(self) -> Optional[str]:
        """Gets the AssetId property"""
        return self.properties.get("AssetId", None)

    @odata(name="ContentMarket")
    @property
    def content_market(self) -> Optional[str]:
        """Gets the ContentMarket property"""
        return self.properties.get("ContentMarket", None)

    @odata(name="VersionString")
    @property
    def version_string(self) -> Optional[str]:
        """Gets the VersionString property"""
        return self.properties.get("VersionString", None)
