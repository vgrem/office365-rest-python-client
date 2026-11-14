from __future__ import annotations

from office365.intune.devices.management.managed.app.status import ManagedAppStatus
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class ManagedAppStatusRaw(ManagedAppStatus):
    @odata(name="content")
    @property
    def content(self) -> Json:
        """Gets the content property"""
        return self.properties.get("content", Json())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppStatusRaw"
