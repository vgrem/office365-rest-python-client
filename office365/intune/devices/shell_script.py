from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.mobileapps.runasaccounttype import RunAsAccountType
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from datetime import timedelta

    from office365.intune.devices.management.script_assignment import DeviceManagementScriptAssignment
    from office365.intune.devices.management.script_device_state import DeviceManagementScriptDeviceState
    from office365.intune.devices.management.script_group_assignment import DeviceManagementScriptGroupAssignment
    from office365.intune.devices.management.script_run_summary import DeviceManagementScriptRunSummary
    from office365.intune.devices.management.script_user_state import DeviceManagementScriptUserState


@version("beta")
class DeviceShellScript(Entity):
    @odata(name="blockExecutionNotifications")
    @property
    def block_execution_notifications(self) -> Optional[bool]:
        """Gets the blockExecutionNotifications property"""
        return self.properties.get("blockExecutionNotifications", None)

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

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="executionFrequency")
    @property
    def execution_frequency(self) -> Optional[timedelta]:
        """Gets the executionFrequency property"""
        return self.properties.get("executionFrequency", None)

    @odata(name="fileName")
    @property
    def file_name(self) -> Optional[str]:
        """Gets the fileName property"""
        return self.properties.get("fileName", None)

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="retryCount")
    @property
    def retry_count(self) -> Optional[int]:
        """Gets the retryCount property"""
        return self.properties.get("retryCount", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="runAsAccount")
    @property
    def run_as_account(self) -> RunAsAccountType:
        """Gets the runAsAccount property"""
        return self.properties.get("runAsAccount", RunAsAccountType.system)

    @odata(name="scriptContent")
    @property
    def script_content(self) -> Optional[bytes]:
        """Gets the scriptContent property"""
        return self.properties.get("scriptContent", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[DeviceManagementScriptAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.management.script_assignment import DeviceManagementScriptAssignment

        return self.properties.get(
            "assignments",
            EntityCollection[DeviceManagementScriptAssignment](
                self.context, DeviceManagementScriptAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @odata(name="deviceRunStates", navigation=True)
    @property
    def device_run_states(self) -> EntityCollection[DeviceManagementScriptDeviceState]:
        """Gets the deviceRunStates property"""
        from office365.intune.devices.management.script_device_state import DeviceManagementScriptDeviceState

        return self.properties.get(
            "deviceRunStates",
            EntityCollection[DeviceManagementScriptDeviceState](
                self.context, DeviceManagementScriptDeviceState, ResourcePath("deviceRunStates", self.resource_path)
            ),
        )

    @odata(name="groupAssignments", navigation=True)
    @property
    def group_assignments(self) -> EntityCollection[DeviceManagementScriptGroupAssignment]:
        """Gets the groupAssignments property"""
        from office365.intune.devices.management.script_group_assignment import DeviceManagementScriptGroupAssignment

        return self.properties.get(
            "groupAssignments",
            EntityCollection[DeviceManagementScriptGroupAssignment](
                self.context, DeviceManagementScriptGroupAssignment, ResourcePath("groupAssignments", self.resource_path)
            ),
        )

    @odata(name="runSummary", navigation=True)
    @property
    def run_summary(self) -> DeviceManagementScriptRunSummary:
        """Gets the runSummary property"""
        from office365.intune.devices.management.script_run_summary import DeviceManagementScriptRunSummary

        return self.properties.get(
            "runSummary", DeviceManagementScriptRunSummary(self.context, ResourcePath("runSummary", self.resource_path))
        )

    @odata(name="userRunStates", navigation=True)
    @property
    def user_run_states(self) -> EntityCollection[DeviceManagementScriptUserState]:
        """Gets the userRunStates property"""
        from office365.intune.devices.management.script_user_state import DeviceManagementScriptUserState

        return self.properties.get(
            "userRunStates",
            EntityCollection[DeviceManagementScriptUserState](
                self.context, DeviceManagementScriptUserState, ResourcePath("userRunStates", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceShellScript"

    @require_permission(
        delegated=["DeviceManagementScripts.ReadWrite.All"],
        application=["DeviceManagementScripts.ReadWrite.All"],
    )
    def assign(
        self,
        device_management_script_group_assignments: ClientValueCollection[DeviceManagementScriptGroupAssignment],
        device_management_script_assignments: ClientValueCollection[DeviceManagementScriptAssignment],
    ) -> Self:
        """assign operation.

        Args:
            device_management_script_group_assignments:
                deviceManagementScriptGroupAssignments parameter
            device_management_script_assignments (ClientValueCollection[DeviceManagementScriptAssignment]):
                deviceManagementScriptAssignments parameter
        """
        qry = ServiceOperationQuery(
            self,
            "assign",
            None,
            {
                "deviceManagementScriptGroupAssignments": device_management_script_group_assignments,
                "deviceManagementScriptAssignments": device_management_script_assignments,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
