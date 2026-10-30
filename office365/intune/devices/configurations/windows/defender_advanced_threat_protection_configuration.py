from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WindowsDefenderAdvancedThreatProtectionConfiguration(Entity):
    @odata(name="allowSampleSharing")
    @property
    def allow_sample_sharing(self) -> Optional[bool]:
        """Gets the allowSampleSharing property"""
        return self.properties.get("allowSampleSharing", None)

    @odata(name="enableExpeditedTelemetryReporting")
    @property
    def enable_expedited_telemetry_reporting(self) -> Optional[bool]:
        """Gets the enableExpeditedTelemetryReporting property"""
        return self.properties.get("enableExpeditedTelemetryReporting", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderAdvancedThreatProtectionConfiguration"
