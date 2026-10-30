from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.artifact import Artifact

if TYPE_CHECKING:
    from office365.security.threatintelligence.host import Host


class PassiveDnsRecord(Entity):
    @odata(name="collectedDateTime")
    @property
    def collected_date_time(self) -> datetime:
        """Gets the collectedDateTime property"""
        return self.properties.get("collectedDateTime", datetime.min)

    @odata(name="firstSeenDateTime")
    @property
    def first_seen_date_time(self) -> datetime:
        """Gets the firstSeenDateTime property"""
        return self.properties.get("firstSeenDateTime", datetime.min)

    @odata(name="lastSeenDateTime")
    @property
    def last_seen_date_time(self) -> datetime:
        """Gets the lastSeenDateTime property"""
        return self.properties.get("lastSeenDateTime", datetime.min)

    @odata(name="recordType")
    @property
    def record_type(self) -> Optional[str]:
        """Gets the recordType property"""
        return self.properties.get("recordType", None)

    @odata(name="artifact", navigation=True)
    @property
    def artifact(self) -> Artifact:
        """Gets the artifact property"""
        return self.properties.get("artifact", Artifact(self.context, ResourcePath("artifact", self.resource_path)))

    @odata(name="parentHost", navigation=True)
    @property
    def parent_host(self) -> Host:
        """Gets the parentHost property"""
        return self.properties.get("parentHost", Host(self.context, ResourcePath("parentHost", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.PassiveDnsRecord"
