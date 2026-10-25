from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AlternateUrl(Entity):
    @odata(name="Uri")
    @property
    def uri(self) -> Optional[str]:
        """Gets the Uri property"""
        return self.properties.get("Uri", None)

    @odata(name="UrlZone")
    @property
    def url_zone(self) -> Optional[int]:
        """Gets the UrlZone property"""
        return self.properties.get("UrlZone", None)
