from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.workflow.setting import WorkflowSetting
from office365.entity import Entity
from office365.runtime.types.odata_property import key, odata


@key("versionNumber")
class WorkflowVersion(Entity):
    @odata(name="versionNumber")
    @property
    def version_number(self) -> Optional[int]:
        """Gets the versionNumber property"""
        return self.properties.get("versionNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.WorkflowVersion"

    @odata(name="settings")
    @property
    def settings(self) -> WorkflowSetting:
        """Gets the settings property"""
        return self.properties.get("settings", WorkflowSetting())
