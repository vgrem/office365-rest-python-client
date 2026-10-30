from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management_export_job import DeviceManagementExportJob


class DeviceManagementReports(Entity):
    """Device management reports entity"""

    @odata(name="exportJobs", navigation=True)
    @property
    def export_jobs(self) -> EntityCollection[DeviceManagementExportJob]:
        """Gets the exportJobs property"""
        from office365.intune.devices.management_export_job import (
            DeviceManagementExportJob,
        )

        return self.properties.get(
            "exportJobs",
            EntityCollection[DeviceManagementExportJob](
                self.context, DeviceManagementExportJob, ResourcePath("exportJobs", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementReports"
