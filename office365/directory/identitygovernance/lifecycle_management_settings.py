from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.emailsettings import EmailSettings
from office365.directory.identitygovernance.quarantine_configuration import QuarantineConfiguration
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class LifecycleManagementSettings(Entity):
    @odata(name="emailSettings")
    @property
    def email_settings(self) -> EmailSettings:
        """Gets the emailSettings property"""
        return self.properties.get("emailSettings", EmailSettings())

    @odata(name="workflowScheduleIntervalInHours")
    @property
    def workflow_schedule_interval_in_hours(self) -> Optional[int]:
        """Gets the workflowScheduleIntervalInHours property"""
        return self.properties.get("workflowScheduleIntervalInHours", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.LifecycleManagementSettings"

    @odata(name="quarantineConfiguration")
    @property
    def quarantine_configuration(self) -> QuarantineConfiguration:
        """Gets the quarantineConfiguration property"""
        return self.properties.get("quarantineConfiguration", QuarantineConfiguration())
