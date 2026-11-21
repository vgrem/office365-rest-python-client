from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.compliance.script_platform_type import DeviceComplianceScriptPlatformType
from office365.intune.devices.management.mobileapps.runasaccounttype import RunAsAccountType
from office365.permissions import require_permission, requires_license
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.compliance.script_device_state import DeviceComplianceScriptDeviceState
    from office365.intune.devices.compliance.script_run_summary import DeviceComplianceScriptRunSummary
    from office365.intune.devices.health_script_assignment import DeviceHealthScriptAssignment


@version("beta")
@requires_license("INTUNE_A")
class DeviceComplianceScript(Entity):
    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="detectionScriptContent")
    @property
    def detection_script_content(self) -> Optional[bytes]:
        """Gets the detectionScriptContent property"""
        return self.properties.get("detectionScriptContent", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="enforceSignatureCheck")
    @property
    def enforce_signature_check(self) -> Optional[bool]:
        """Gets the enforceSignatureCheck property"""
        return self.properties.get("enforceSignatureCheck", None)

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="platform")
    @property
    def platform(self) -> Optional[DeviceComplianceScriptPlatformType]:
        """Gets the platform property"""
        return self.properties.get("platform", None)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="runAs32Bit")
    @property
    def run_as32_bit(self) -> Optional[bool]:
        """Gets the runAs32Bit property"""
        return self.properties.get("runAs32Bit", None)

    @odata(name="runAsAccount")
    @property
    def run_as_account(self) -> RunAsAccountType:
        """Gets the runAsAccount property"""
        return self.properties.get("runAsAccount", RunAsAccountType.system)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[DeviceHealthScriptAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.health_script_assignment import DeviceHealthScriptAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[DeviceHealthScriptAssignment](
                self.context, DeviceHealthScriptAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="deviceRunStates", navigation=True)
    @property
    def device_run_states(self) -> EntityCollection[DeviceComplianceScriptDeviceState]:
        """Gets the deviceRunStates property"""
        from office365.intune.devices.compliance.script_device_state import DeviceComplianceScriptDeviceState

        return self.properties.get(
            "deviceRunStates",
            EntityCollection[DeviceComplianceScriptDeviceState](
                self.context, DeviceComplianceScriptDeviceState, ResourcePath("deviceRunStates", self.resource_path)
            ),
        )

    @odata(name="runSummary", navigation=True)
    @property
    def run_summary(self) -> DeviceComplianceScriptRunSummary:
        """Gets the runSummary property"""
        from office365.intune.devices.compliance.script_run_summary import DeviceComplianceScriptRunSummary

        return self.properties.get(
            "runSummary", DeviceComplianceScriptRunSummary(self.context, ResourcePath("runSummary", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceComplianceScript"

    @require_permission(
        delegated=["DeviceManagementScripts.ReadWrite.All"],
        application=["DeviceManagementScripts.ReadWrite.All"],
    )
    def assign(self, device_health_script_assignments: ClientValueCollection[DeviceHealthScriptAssignment]) -> Self:
        """assign operation.

        Args:
            device_health_script_assignments (ClientValueCollection[DeviceHealthScriptAssignment]):
                deviceHealthScriptAssignments parameter
        """
        qry = ServiceOperationQuery(
            self, "assign", None, {"deviceHealthScriptAssignments": device_health_script_assignments}, None, None
        )
        self.context.add_query(qry)
        return self
