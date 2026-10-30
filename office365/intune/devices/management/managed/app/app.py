from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.compliance.managedappavailability import ManagedAppAvailability
from office365.runtime.types.odata_property import odata


class ManagedApp(Entity):
    @odata(name="appAvailability", readonly=True)
    @property
    def app_availability(self) -> ManagedAppAvailability:
        """Gets the appAvailability property"""
        return self.properties.get("appAvailability", ManagedAppAvailability.global_)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedApp"
