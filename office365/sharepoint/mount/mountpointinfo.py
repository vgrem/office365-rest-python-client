from typing import Optional

from office365.sharepoint.entity import Entity


class MountPointInfo(Entity):
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def redirect_url(self) -> Optional[str]:
        """Gets the RedirectUrl property"""
        return self.properties.get("RedirectUrl", None)
