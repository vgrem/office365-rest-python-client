from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.health_script_parameter import DeviceHealthScriptParameter
from office365.intune.devices.health_script_type import DeviceHealthScriptType
from office365.intune.devices.management.mobileapps.runasaccounttype import RunAsAccountType
from office365.permissions import require_permission, requires_license
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.health_script_assignment import DeviceHealthScriptAssignment
    from office365.intune.devices.health_script_device_state import DeviceHealthScriptDeviceState
    from office365.intune.devices.health_script_run_summary import DeviceHealthScriptRunSummary


@version("beta")
@requires_license("INTUNE_A")
class DeviceHealthScript(Entity):
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

    @odata(name="detectionScriptParameters")
    @property
    def detection_script_parameters(self) -> ClientValueCollection[DeviceHealthScriptParameter]:
        """Gets the detectionScriptParameters property"""
        return self.properties.get(
            "detectionScriptParameters", ClientValueCollection[DeviceHealthScriptParameter](DeviceHealthScriptParameter)
        )

    @odata(name="deviceHealthScriptType")
    @property
    def device_health_script_type(self) -> Optional[DeviceHealthScriptType]:
        """Gets the deviceHealthScriptType property"""
        return self.properties.get("deviceHealthScriptType", None)

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

    @odata(name="highestAvailableVersion")
    @property
    def highest_available_version(self) -> Optional[str]:
        """Gets the highestAvailableVersion property"""
        return self.properties.get("highestAvailableVersion", None)

    @odata(name="isGlobalScript")
    @property
    def is_global_script(self) -> Optional[bool]:
        """Gets the isGlobalScript property"""
        return self.properties.get("isGlobalScript", None)

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @odata(name="remediationScriptContent")
    @property
    def remediation_script_content(self) -> Optional[bytes]:
        """Gets the remediationScriptContent property"""
        return self.properties.get("remediationScriptContent", None)

    @odata(name="remediationScriptParameters")
    @property
    def remediation_script_parameters(self) -> ClientValueCollection[DeviceHealthScriptParameter]:
        """Gets the remediationScriptParameters property"""
        return self.properties.get(
            "remediationScriptParameters",
            ClientValueCollection[DeviceHealthScriptParameter](DeviceHealthScriptParameter),
        )

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
    def device_run_states(self) -> EntityCollection[DeviceHealthScriptDeviceState]:
        """Gets the deviceRunStates property"""
        from office365.intune.devices.health_script_device_state import DeviceHealthScriptDeviceState

        return self.properties.get(
            "deviceRunStates",
            EntityCollection[DeviceHealthScriptDeviceState](
                self.context, DeviceHealthScriptDeviceState, ResourcePath("deviceRunStates", self.resource_path)
            ),
        )

    @odata(name="runSummary", navigation=True)
    @property
    def run_summary(self) -> DeviceHealthScriptRunSummary:
        """Gets the runSummary property"""
        from office365.intune.devices.health_script_run_summary import DeviceHealthScriptRunSummary

        return self.properties.get(
            "runSummary", DeviceHealthScriptRunSummary(self.context, ResourcePath("runSummary", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceHealthScript"

    @require_permission(
        delegated=[
            "DeviceManagementScripts.ReadWrite.All",
        ],
        application=[
            "DeviceManagementScripts.ReadWrite.All",
        ],
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

    @require_permission(
        delegated=[
            "DeviceManagementScripts.Read.All",
            "DeviceManagementScripts.ReadWrite.All",
        ],
        application=[
            "DeviceManagementScripts.Read.All",
            "DeviceManagementScripts.ReadWrite.All",
        ],
    )
    def get_global_script_highest_available_version(self) -> ClientResult[str]:
        """getGlobalScriptHighestAvailableVersion operation."""
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "getGlobalScriptHighestAvailableVersion", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=[
            "DeviceManagementScripts.ReadWrite.All",
        ],
        application=[
            "DeviceManagementScripts.ReadWrite.All",
        ],
    )
    def update_global_script(self, version: str) -> ClientResult[str]:
        """updateGlobalScript operation.

        Args:
            version (str):
                version parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "updateGlobalScript", None, {"version": version}, None, return_type)
        self.context.add_query(qry)
        return return_type
