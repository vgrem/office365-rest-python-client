from __future__ import annotations

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.mobileapps.contained_app import MobileContainedApp
from office365.runtime.paths.resource_path import ResourcePath


class MobileAppContent(Entity):
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
