from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MobileAppCatalogPackage(Entity):
    @odata(name="productDescription", readonly=True)
    @property
    def product_description(self) -> Optional[str]:
        """Gets the productDescription property"""
        return self.properties.get("productDescription", None)

    @odata(name="productDisplayName", readonly=True)
    @property
    def product_display_name(self) -> Optional[str]:
        """Gets the productDisplayName property"""
        return self.properties.get("productDisplayName", None)

    @odata(name="productId", readonly=True)
    @property
    def product_id(self) -> Optional[str]:
        """Gets the productId property"""
        return self.properties.get("productId", None)

    @odata(name="publisherDisplayName", readonly=True)
    @property
    def publisher_display_name(self) -> Optional[str]:
        """Gets the publisherDisplayName property"""
        return self.properties.get("publisherDisplayName", None)

    @odata(name="versionDisplayName", readonly=True)
    @property
    def version_display_name(self) -> Optional[str]:
        """Gets the versionDisplayName property"""
        return self.properties.get("versionDisplayName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppCatalogPackage"
