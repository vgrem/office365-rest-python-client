from office365.admin.sharepoint.settings import SharepointSettings
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class Sharepoint(Entity):
    """A container for administrative resources to manage tenant-level settings for SharePoint and OneDrive."""

    @odata(name="settings", navigation=True)
    @property
    def settings(self) -> SharepointSettings:
        """Represents the tenant-level settings for SharePoint and OneDrive."""
        return self.properties.get(
            "settings",
            SharepointSettings(self.context, ResourcePath("settings", self.resource_path)),
        )
