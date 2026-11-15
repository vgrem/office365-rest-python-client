from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MountPointInfo(Entity):
    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="RedirectUrl")
    @property
    def redirect_url(self) -> Optional[str]:
        """Gets the RedirectUrl property"""
        return self.properties.get("RedirectUrl", None)
