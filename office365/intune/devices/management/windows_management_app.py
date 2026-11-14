from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.common.managed_installer_status import ManagedInstallerStatus
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.windows_management_app_health_state import WindowsManagementAppHealthState


@version("beta")
class WindowsManagementApp(Entity):
    @odata(name="availableVersion")
    @property
    def available_version(self) -> Optional[str]:
        """Gets the availableVersion property"""
        return self.properties.get("availableVersion", None)

    @odata(name="managedInstallerConfiguredDateTime")
    @property
    def managed_installer_configured_date_time(self) -> Optional[str]:
        """Gets the managedInstallerConfiguredDateTime property"""
        return self.properties.get("managedInstallerConfiguredDateTime", None)

    @odata(name="healthStates", navigation=True)
    @property
    def health_states(self) -> EntityCollection[WindowsManagementAppHealthState]:
        """Gets the healthStates property"""
        from office365.intune.devices.management.windows_management_app_health_state import (
            WindowsManagementAppHealthState,
        )

        return self.properties.get(
            "healthStates",
            EntityCollection[WindowsManagementAppHealthState](
                self.context, WindowsManagementAppHealthState, ResourcePath("healthStates", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagementApp"

    @require_permission(
        delegated=[
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementApps.Read.All",
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def set_as_managed_installer(self) -> Self:
        """setAsManagedInstaller operation."""
        qry = ServiceOperationQuery(self, "setAsManagedInstaller", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="managedInstaller")
    @property
    def managed_installer(self) -> Optional[ManagedInstallerStatus]:
        """Gets the managedInstaller property"""
        return self.properties.get("managedInstaller", None)
