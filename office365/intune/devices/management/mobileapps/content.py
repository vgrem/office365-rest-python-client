from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.mobileapps.contained_app import (
    MobileContainedApp,
)
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.mobileapps.content_file import (
        MobileAppContentFile,
    )


class MobileAppContent(Entity):
    @odata(name="containedApps", navigation=True)
    @property
    def contained_apps(self) -> EntityCollection[MobileContainedApp]:
        """Gets the containedApps property"""
        return self.properties.get(
            "containedApps",
            EntityCollection[MobileContainedApp](
                self.context, MobileContainedApp, ResourcePath("containedApps", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppContent"

    @odata(name="files", navigation=True)
    @property
    def files(self) -> EntityCollection[MobileAppContentFile]:
        """Gets the files property"""
        from office365.intune.devices.management.mobileapps.content_file import (
            MobileAppContentFile,
        )

        return self.properties.get(
            "files",
            EntityCollection[MobileAppContentFile](
                self.context, MobileAppContentFile, ResourcePath("files", self.resource_path)
            ),
        )
