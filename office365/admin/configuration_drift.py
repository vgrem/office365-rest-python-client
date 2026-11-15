from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.admin.drift_status import DriftStatus
from office365.directory.drifted_property import DriftedProperty
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.teams.members.open_complex_dictionary_type import OpenComplexDictionaryType


class ConfigurationDrift(Entity):
    @odata(name="baselineResourceDisplayName", readonly=True)
    @property
    def baseline_resource_display_name(self) -> Optional[str]:
        """Gets the baselineResourceDisplayName property"""
        return self.properties.get("baselineResourceDisplayName", None)

    @odata(name="driftedProperties", readonly=True)
    @property
    def drifted_properties(self) -> ClientValueCollection[DriftedProperty]:
        """Gets the driftedProperties property"""
        return self.properties.get("driftedProperties", ClientValueCollection[DriftedProperty](DriftedProperty))

    @odata(name="firstReportedDateTime", readonly=True)
    @property
    def first_reported_date_time(self) -> Optional[datetime]:
        """Gets the firstReportedDateTime property"""
        return self.properties.get("firstReportedDateTime", datetime.min)

    @odata(name="monitorId", readonly=True)
    @property
    def monitor_id(self) -> Optional[str]:
        """Gets the monitorId property"""
        return self.properties.get("monitorId", None)

    @odata(name="resourceInstanceIdentifier", readonly=True)
    @property
    def resource_instance_identifier(self) -> OpenComplexDictionaryType:
        """Gets the resourceInstanceIdentifier property"""
        return self.properties.get("resourceInstanceIdentifier", OpenComplexDictionaryType())

    @odata(name="resourceType", readonly=True)
    @property
    def resource_type(self) -> Optional[str]:
        """Gets the resourceType property"""
        return self.properties.get("resourceType", None)

    @odata(name="status", readonly=True)
    @property
    def status(self) -> DriftStatus:
        """Gets the status property"""
        return self.properties.get("status", DriftStatus.active)

    @odata(name="tenantId", readonly=True)
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConfigurationDrift"
