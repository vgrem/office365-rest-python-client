from typing import Optional

from office365.sharepoint.entity import Entity


class App(Entity):
    @property
    def asset_id(self) -> Optional[str]:
        """Gets the AssetId property"""
        return self.properties.get("AssetId", None)

    @property
    def content_market(self) -> Optional[str]:
        """Gets the ContentMarket property"""
        return self.properties.get("ContentMarket", None)

    @property
    def version_string(self) -> Optional[str]:
        """Gets the VersionString property"""
        return self.properties.get("VersionString", None)
