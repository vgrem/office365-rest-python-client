from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.configuration_baseline import ConfigurationBaseline
    from office365.directory.identity_set import IdentitySet
    from office365.security.monitor_mode import MonitorMode
    from office365.security.monitor_status import MonitorStatus
    from office365.teams.members.open_complex_dictionary_type import (
        OpenComplexDictionaryType,
    )


class ConfigurationMonitor(Entity):
    @odata(name="createdBy", readonly=True)
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="inactivationReason", readonly=True)
    @property
    def inactivation_reason(self) -> Optional[str]:
        """Gets the inactivationReason property"""
        return self.properties.get("inactivationReason", None)

    @odata(name="lastModifiedBy", readonly=True)
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="mode")
    @property
    def mode(self) -> MonitorMode:
        """Gets the mode property"""
        from office365.security.monitor_mode import MonitorMode

        return self.properties.get("mode", MonitorMode.monitorOnly)

    @odata(name="monitorRunFrequencyInHours", readonly=True)
    @property
    def monitor_run_frequency_in_hours(self) -> Optional[int]:
        """Gets the monitorRunFrequencyInHours property"""
        return self.properties.get("monitorRunFrequencyInHours", None)

    @odata(name="parameters")
    @property
    def parameters(self) -> OpenComplexDictionaryType:
        """Gets the parameters property"""
        from office365.teams.members.open_complex_dictionary_type import (
            OpenComplexDictionaryType,
        )

        return self.properties.get("parameters", OpenComplexDictionaryType())

    @odata(name="status", readonly=True)
    @property
    def status(self) -> MonitorStatus:
        """Gets the status property"""
        from office365.security.monitor_status import MonitorStatus

        return self.properties.get("status", MonitorStatus.active)

    @odata(name="tenantId", readonly=True)
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="baseline", navigation=True)
    @property
    def baseline(self) -> ConfigurationBaseline:
        """Gets the baseline property"""
        from office365.common.configuration_baseline import ConfigurationBaseline

        return self.properties.get(
            "baseline", ConfigurationBaseline(self.context, ResourcePath("baseline", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConfigurationMonitor"
